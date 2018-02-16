# -*- coding: utf-8 -*-
from  Util import  *
import jsonmodel_decoder


def output_json2field():
    lines =  readlines_from_stdin()
    classname = lines[0].strip('\n').strip(' ')
    s = ''.join(lines[1:])

    jsonmodel_decoder.make_json(json.loads(s),classname)
 

