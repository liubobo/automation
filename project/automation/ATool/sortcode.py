# -*- coding: utf-8 -*-
__author__ = 'liubo'
from Util import *

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

def sortcode():

    lines = readlines_from_stdin()
    joinedStr = ''.join(lines) 

    if '#import' in joinedStr or '#include' in joinedStr:
        sortImport(lines)
    else:
        lines.sort(key=lambda x: len(x)) #a b c ,last len
        map(print_obj,lines)





