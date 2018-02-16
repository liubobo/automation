# -*- coding: utf-8 -*-
__author__ = 'liubo'
from Util import *

def sortcode():
    lines = readlines_from_stdin()
    lines.sort(key=lambda x: len(x))
    map(print_obj,lines)

