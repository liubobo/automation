# from ios_code_generator import getter
from util import *
from viewLists import vList as availables

def getProps(rline):
    rline = str(line).strip('\n').strip(' ')
    splitList = filter(lambda m: len(m.strip(' ')), re.split(r'[;,\s]\s*', rline))
    if len(splitList) >= 2:
        stype = splitList[0]
        if stype == 's':
            stype = 'NSSTring'
        if stype == 'a':
            stype = 'NSArray'
        if stype == 'd':
            stype = 'NSDictionary'

        return '@property(nonatomic, strong) {} *{};'.format(stype, splitList[1])
    else:
        try:
            vtype = filter(lambda v: rline.endswith(v.replace('UI', '')), availables)[0]
            return '@property(nonatomic, strong) {} *{};'.format(vtype, rline)
        except:
            return '@property(nonatomic, strong) {} *{};'.format('<#type#>', rline)

for line in readlines_from_stdin():
    print  getProps(line)
