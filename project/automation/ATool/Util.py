import os,sys
import json
import re
import json
import copy
from viewLists import vList
from io import StringIO

reload(sys)
sys.setdefaultencoding( "utf-8" )

def render_template(template_filename, context):
	from jinja2 import Environment, FileSystemLoader
	PATH = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_ENVIRONMENT = Environment(
	    autoescape=False,
	    loader=FileSystemLoader(os.path.join(PATH, './templates')),
	    trim_blocks=False)
	return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def is_ui(vtype):
    if vtype in vList:
        return True
    return False

def simulate(str):
    strio = StringIO(str)
    sys.stdin = strio

def toCap(x):
      return ''.join([x[0].upper(), x[1:]])


def myLow(x):
    return ''.join([x[0].lower(), x[1:]])

def  hasAttrib(self, name):
 try:
      r=object.__getattribute__(self, name)
 except:
      r=None
 return r

def find_type(root):
    # cell
    for cell in root.iter("tableViewCell"):
        if cell is not None:
            file_type = 'Cell'
    #vc
    for country in root.iter("placeholder"):
        for connections in country:
                if connections is not None:
                    file_type = 'ViewController'
        file_type = 'View'

def prn_obj(obj):
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def print_obj(obj):
    print obj

def tab(lines,n):
    return '\t'+('\t'*n).join(map(lambda x :x.strip()+'\n',lines.split('\n')))


def readlines_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if isinstance(line, str):
            line = line.decode(encoding='utf-8')
        lines.append(line)
    return lines