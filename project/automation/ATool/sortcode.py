# -*- coding: utf-8 -*-
__author__ = 'liubo'
from Util import *
import re
def sortbyLen(lines):

    lines.sort(key=lambda x: len(x))  # a b c ,last len
    if len(lines) == 0:
        return
    map(print_obj, lines)
    print '\n'+' '


def sortImport(lines):
    arr_import = []
    arr_include = []
    arr_third = []
    arr_category = []

    for line  in lines:
          if '+' in line:
              arr_category.append(line)
              continue
          if '<' in line:
              arr_third.append(line)
              continue
          if '#import' in line:
              arr_import.append(line)
              continue
          if '#include' in line:
               arr_include.append(line)
               continue

    sortbyLen(arr_import)
    sortbyLen(arr_category)
    sortbyLen(arr_include)
    sortbyLen(arr_third)

def takeSecond(elem):
    return elem.keys()[0]

def sortcode():

    lines = readlines_from_stdin()
    joinedStr = ''.join(lines)

    if '@property' in joinedStr:
        alist = map(lambda l: {l.split(')')[1].split('*')[0]: l}, lines)
        if len(set(map(lambda l: l.split(')')[1].split('*')[0].strip(), lines))) == 1:
            lines.sort(key=lambda x: len(x))  # a b c ,last len
            map(print_obj, lines)
            return

        print '\n'.join(map(lambda x: x.values()[0], alist))
        return

    if len(re.findall(r'''^\w.*\*.*''', joinedStr)):
       alist = map(lambda l:{l.split('*')[0]:l},lines)
       if  len(set(map(lambda l: l.split('*')[0].strip(), lines))) ==1:
           lines.sort(key=lambda x: x)  # a b c ,last len
           map(print_obj, lines)
           return
       alist.sort(key=takeSecond)
       print '\n'.join(map(lambda x:x.values()[0],alist))
       return

    if '#import' in joinedStr or '#include' in joinedStr:
        sortImport(lines)

    else:
        lines.sort(key=lambda x: len(x)) #a b c ,last len
        map(print_obj,lines)


# simulate(u'''
#     UIView *_xuzhiView;//投保须知
#     UIView *_line;
#     UIView *_fourItemsView;
# ''')
#
#
# sortcode()