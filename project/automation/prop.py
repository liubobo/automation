# from ios_code_generator import getter
from util import *
from viewLists import vList as availables

for line in readlines_from_stdin():
    rline = str(line).strip('\n').strip(' ')
    splitList = filter(lambda m:len(m.strip(' ')), re.split(r'[;,\s]\s*', rline))

    if len(splitList) >= 2:
        print '@property(nonatomic, strong) {} *{};'.format(splitList[0], splitList[1])
    else:
        try:
            vtype = filter(lambda v:rline.endswith(v.replace('UI', '')), availables)[0]
            print '@property(nonatomic, strong) {} *{};'.format(vtype, rline)
        except:
            print '@property(nonatomic, strong) {} *{};'.format('<#type#>', rline)
