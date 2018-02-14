# from ios_code_generator import getter
from util import *
from viewLists import vList as availables
# simulate(u'mmUITableView')
def getProps(rline):
    propStar = '*'
    propWs = 'strong'
    rline = str(line).strip('\n').strip(' ')
    splitList = filter(lambda m: len(m.strip(' ').strip(';')), re.split(r'[;,\s]\s*', rline))
    assinlist = ['int','double','float','NSInteger','CGFloat','CGRect','CGPoint','bool','BOOL']

    if len(splitList) >= 2:
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
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',splitList[1]+propStar+'Array')
        if stype == 'UITableView':
            yield '@property(nonatomic, {}) {} {}{};'.format(propWs,'NSMutableArray',splitList[1]+propStar+'Array')
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
            yield '@property(nonatomic, strong) {} *{};'.format('<#type#>',propStar,rline)

for line in readlines_from_stdin():
    for x   in   getProps(line):
        print x


'''
test 
mmUITableView  
NSMutableArray
a list
md adict 
s sss 
ma sss
kk
xxCollectionView
int kkk
BOOL kkkkfd

'''