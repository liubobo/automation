# -*- coding: utf-8 -*-
__author__ = 'liubo'
from Util import *
import re

def isListSorted_sorted(lst):
    return sorted(lst) == lst or sorted(lst, reverse=True) == lst

def sortcode():
    lines = readlines_from_stdin()

    if isListSorted_sorted(lines):
        lines.sort(key=lambda x: len(x))  # a b c ,last len
        map(print_obj, lines)
    else:
        print '\n'.join(sorted(lines))


