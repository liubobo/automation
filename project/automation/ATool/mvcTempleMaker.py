from Util import *
import props
import getters

def get_type_name(input_lines):
    for line in input_lines:
         for rline in props.getProps(line):
            mtype = filter(lambda x: len(x), re.split(r'[;,\s ]\s*', rline))[2].replace('*', '')
            name = filter(lambda x: len(x), re.split(r'[;,\s ]\s*', rline))[3].replace('*', '')

            sf = ''
            try:
                sf = filter(lambda x: len(x), re.split(r'[;,\s ]\s*', line))[2].replace('*', '')
            except:
                sf = 'self.view'
            yield (mtype,name,sf)

def get_protocols(input_lines):
    protocols = ''
    controls = []
    delgates = ['UITableViewDelegate,UITableViewDataSource', 'UITextFieldDelegate', 'UITextViewDelegate']
    for vtype, name ,x in get_type_name(input_lines):
        for d in delgates:
            if d.startswith(vtype):
                controls.append(d)
    if len(controls):
        protocols = '<' + ','.join(set(controls)) + '>'
    return protocols

def addSubViews(input_lines):

    subviews = []
    for vtype, name,pa in get_type_name(input_lines):
        if is_ui(vtype):
            subviews.append('\t[{} addSubview:self.{}];'.format(pa,name))
    return '\n'.join(subviews)


def get_props_all(l):
    propall = []
    for line in l:
        for x   in   props.getProps(line):
            propall.append(x)
    return '\n'.join(propall)

def get_getters(l):
    getterlist = []
    for line in l:
        for x   in   props.getProps(line):
            if x is None:
                yield ''
            else:
                if getters.gen_getter(x) is None:
                    yield ''
                else:
                    yield  getters.gen_getter(x)

def get_buttons(l):
    buttons = filter(lambda (vtype,name,pa):vtype=='UIButton',get_type_name(l))

    return map(lambda x:x[1],buttons)

def get_masornys(l):
    masornys = filter(lambda (vtype,name,pa):is_ui(vtype),get_type_name(l))
    return masornys



def output_type(mtype):

    lines  = readlines_from_stdin()
    name  = lines[0]
    uiNames = lines[1:]

    render_getter = get_getters(uiNames)
    result = ''
    for x in render_getter:
        count = 0
        for y in x.split('\n'):
            count += 1
            if count >= 8 and not (y.strip() == '}') and not (y.strip().startswith('return')):
                # print count
                result+= '\t\t' + y+'\n'
            else:
                result += y+'\n'

    html =  render_template(mtype+'.html',{'name':name,
                            'protocols':get_protocols(uiNames),
                            'props':get_props_all(uiNames),
                            'subviews':addSubViews(uiNames),
                            'buttons':get_buttons(uiNames),
                            'hasProtocls':'Table' in get_protocols(uiNames),
                            'masornys':get_masornys(uiNames) ,
                            'hasmas':False,
                            'getters':result
                            })

    if mtype == 'cell':
        html = html.replace('self.view','self.contentView')
    if mtype == 'v':
        html = html.replace('self.view', 'self')

    print html


