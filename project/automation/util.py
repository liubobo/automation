#encoding=utf-8
import sys,os
import json
import re
import json
import copy
from io import StringIO
import jsonmodel_decoder
reload(sys)
sys.setdefaultencoding( "utf-8" )

def simulate(str):
    strio = StringIO(str)
    sys.stdin = strio

def myCap(x):
      return ''.join([x[0].upper(), x[1:]])

def  hasAttrib(self, name):
 try:
      r=object.__getattribute__(self, name)
 except:
      r=None
 return r

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

def print_obj(obj):
 	print obj

def render_template(template_filename, context):
	from jinja2 import Environment, FileSystemLoader
	PATH = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_ENVIRONMENT = Environment(
	    autoescape=False,
	    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
	    trim_blocks=False)
	return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


#表达式正则节省了几十行判断代码,捕获多个大写的情况
def getControlType(result):
    mtype = 'costom'
    matches = re.finditer(r"[A-Z][a-z]*(?=;)", result+';')

    for matchNum, match in enumerate(matches):
        mtype = match.group().lower()
    if mtype == 'field':
        return 'textField'
    return mtype

def gen_protocols(controls):
    protocolStr = ''
    protocols = []

    for control in controls:
        control = control.decode(encoding='utf-8').strip('\n').strip(' ')
        if str(control).endswith('TableView'):
            protocols.append('UITableViewDataSource,UITableViewDelegate')
        if str(control).endswith('TextField'):
            protocols.append('UITextFieldDelegate')
        if str(control).endswith('TextView'):
            protocols.append('UITextViewDelegate')
    if len(controls):
        protocolStr += '<' + ','.join(protocols) + '>'
    return protocolStr


def gen_props(controls):
    props = ''
    for result in controls:
        if (getControlType(result) == 'costom'):
            props += '@property(nonatomic, strong)' +'<#type#>' +' *'+result+';\n';
        regex = r"[A-Z][a-z].*"
        matches = re.finditer(regex, result)
        for matchNum, match in enumerate(matches):
            props += '@property(nonatomic, strong)' + 'UI' +  myCap(getControlType(result))+ ' *' + str(result) + ';' + '\n'
    return props

def gen_subViews(controls):
    subviews = ''

    for result in controls:
        subviews += '\t[self addSubview:self.' + result + '];' + '\n';
    return subviews

def gen_subViewByType(controls,vtype):
    vprent = 'self'
    if vtype == 'tableViewCell':
        vprent = 'self.contentView'
    if vtype == 'viewController':
        vprent = 'self.view'

    subviews = ''
    for result in controls:
        if getControlType(result) == 'costom':
            subviews +=''
        else:
            subviews += '\t\t['+vprent +' addSubview:self.' + result + '];' + '\n';
    return subviews


def gen_event(controls):
    buttons = []
    getters = ''
    for result in controls:
        if str(result).endswith('Button'):
            buttons.append(result)
        html = render_template(getControlType(result) + '.html', {'name': result})
        getters += html + '\n'
    return buttons, getters

def gen_rect(name,view):
    if hasAttrib(view,'rect'):
        return name+'.rect = ' + 'CGReactMake('+view.rect.x +','+view.rect.y+','+view.rect.width+','+view.rect.height+')'

def gen_events(controls,objs):
    buttons = []
    getters = ''
    for l in zip(controls,objs):
        result = l[0]
        v = l[1]
        if str(result).endswith('Button'):
            buttons.append(result)
        html = render_template(getControlType(result) + '.html', {'name': '_'+result,'rect':gen_rect(result,v)})
        getters += html + '\n'
    return buttons, getters


def gen_Temple(m_type):

    lines = readlines_from_stdin()
    name = lines[0]
    controls = lines[1:]
    protocolStr = gen_protocols(controls) if gen_protocols(controls)!='<>' else ''
    props = gen_props(controls)

    vtype = 'view'
    if name.lower().endswith('cell'):
        vtype = 'tableViewCell'
    if name.lower().endswith('viewcontroller'):
        vtype = 'viewController'

    subviews = gen_subViewByType(controls,vtype)
    buttons, getters = gen_event(controls)


    context = {'name': name,
               'controls': filter(lambda v:getControlType(v)!='costom',controls),
               'protocolStr': protocolStr,
               'props': props,
               'subviews': subviews,
               'hasProtocls': len(protocolStr)>len('Delegate'),
               'buttons': buttons,
               'getters': getters
               }
    print render_template(m_type + '.html', context)


    # raise Exception(line)
    #    os.system("pbpaste > m.txt")











