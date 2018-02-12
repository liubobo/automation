import os
import sys
from io import StringIO

reload(sys)
sys.setdefaultencoding( "utf-8" )


def get_filetype(file_path):

    filetypelist = ['Cell', 'View', 'ViewController']
    xibName = os.path.basename(file_path).split('.')[0]
    fileType = 'View'
    try:
        fileType = filter(lambda x: xibName.endswith(x), filetypelist)[0]
    except:
        fileType = 'View'
    return  fileType;

def simulate(str):
    strio = StringIO(str)
    sys.stdin = strio


def toCap(x):
    return ''.join([x[0].upper(), x[1:]])

def hasAttrib(self, name):
    try:
        r = object.__getattribute__(self, name)
    except:
        r = None
    return r

def render_template(template_filename, context):
	from jinja2 import Environment, FileSystemLoader
	PATH = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_ENVIRONMENT = Environment(
	    autoescape=False,
	    loader=FileSystemLoader(os.path.join(PATH, 'uis')),
	    trim_blocks=False)
	return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

