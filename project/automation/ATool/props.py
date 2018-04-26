#encoding=utf-8
import re
from Util import *
from  viewLists import vList as availables
def getProps(line):
    propStar = '*'
    propWs = 'strong'
    rline = str(line).strip('\n').strip(' ')
    splitList = filter(lambda m: len(m.strip(' ').strip(';')), re.split(r'[;,\s]\s*', rline))
    assinlist = ['int','double','float','NSInteger','CGFloat','CGRect','CGPoint','bool','BOOL']
    if rline.startswith('/'):
        yield rline
    elif len(splitList) >= 2:
        stype = splitList[0]
        if stype in assinlist:
            propWs = 'assign'
            propStar = ''
        if stype == 's':
            stype = 'NSString'
        if stype == 'a':
            stype = 'NSArray'
        if stype == 'd':
            stype = 'NSDictionary'
        if stype == 'ms':
            stype = 'NSMutableString'
        if stype == 'ma':
            stype = 'NSMutableArray'
        if stype == 'md':
            stype = 'NSMutableDictionary'
        if type == 'UICollectionView':
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',splitList[1],propStar+'Array')
        if stype == 'UITableView':
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',propStar,splitList[1]+'Array')
        yield '@property(nonatomic, {}) {} {}{};'.format(propWs,stype,propStar, splitList[1])

    else:
        try:
            vtype = filter(lambda v: rline.endswith(v.replace('UI', '')), availables)[0]
            if vtype in assinlist:
                propWs = 'assign'
                propStar = ''

            if vtype == 'UITableView':
                yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',propStar, rline + 'Array')
            if type == 'UICollectionView':
                yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',propStar, splitList[1] + 'Array')
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,vtype,propStar, rline)
        except:
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'<#type#>',propStar,rline)



def output_props(inputs=[]):

    if(len(inputs)==0):
        for line in readlines_from_stdin():
            for x   in   getProps(line):
                print x
    else:
        for line in inputs:
            for x in getProps(line):
                print x

'''
//s 代码字符串 a 表示array d 表示dict 加m表示可变
s str
ms mstr
a array
ma  marray
d  dict
md mdict

//如果自己加类型，就默认生成
int kkk
BOOL kkkkfd
ViewController sss

//不加类型按照UI类型解析
aButton
bLabel
mmUITableView
xxCollectionView

//不是UI类型，就默认给个type填充
custom
custom2


'''