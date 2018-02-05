# -*- coding: utf-8 -*-
from  util import  *
lines =  readlines_from_stdin()
classname = lines[0].strip('\n').strip(' ')
s = ''.join(lines[1:])

jsonmodel_decoder.make_json(json.loads(s),classname)
 

