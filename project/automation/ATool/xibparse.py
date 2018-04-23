#encoding=utf-8
import string,os
from  Util import  *
from UI import UI
import mvcTempleMaker
from  mydict import MyDict as my
import xml.etree.ElementTree as etree
from  automation.ATool.viewLists import vList as availables

file_type = 'View'

def find_type(root):
    # cell

    for cell in root.iter("tableViewCell"):
        if cell is not None:
            return 'Cell'
    #vc
    for country in root.iter("placeholder"):
        for connections in country:
                if connections is not None:
                    return  'ViewController'
    return 'View'


def get_root(file_path):

    tree = etree.parse(file_path)
    root = tree.getroot()
    file_type = find_type(root)

    return root

def convent_dict2ui(child):
    ui = UI()
    ui.id = child.attrib.get('id')
    ui.frame = 'CGRectMake(0,0,0,0)'
    ui.parent = None
    ui.type = child.tag
    ui.name = ui.id + '_' + toCap(child.tag)
    if  child.attrib.get('userLabel'):
        ui.name =  child.attrib.get('userLabel')+toCap(child.tag)
    ui.masonry = ''
    ui.color = ''
    ui.uselabel = ''
    ui.props = child
    return ui
def find_uis(root):
    ui_list = []
    uis = []
    for child in root.iter():
        if child is None: continue
        if str('UI' + toCap(child.tag)) in availables:
            ui = convent_dict2ui(child)
            ui_list.append(ui)
            uis.append(child)
    return  ui_list,uis
def set_view_name(root, ui_list):
    for outlet in root.iter():
        if outlet.tag == 'outlet':
            v_id = outlet.attrib.get('destination')
            v_name = outlet.attrib.get('property')
            v = filter(lambda v: v.id == v_id, ui_list)[0]
            v.name = v_name
def find_ui_byid(vid,ui_list):
    try:
        return filter(lambda v:v.id == vid,ui_list)[0]
    except:
        return None
def prn_obj(obj):
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def parse(root):

    ui_list,ui_trees= find_uis(root)
    set_view_name(root, ui_list)
    allconstraints = []
    allconstraints = filter(lambda constraint:(constraint.tag == 'constraint'),root.iter())
    for node in ui_trees:
        if node is None:continue
        #fist treavel
        # print  node.tag
        # print '*' * 100

        v = find_ui_byid(node.attrib.get('id'), ui_list)
        for subnode in node:
            if subnode is None:continue
            # print subnode.tag
            if subnode.tag == 'rect':
                rect = my(subnode.attrib)
                v.frame = 'CGRectMake('+','.join([rect.x,rect.y,rect.width,rect.height])+')'

            if subnode.tag == 'color':
                color = my(subnode.attrib)
                v.backgroundColor = [color.green,color.red,color.blue,color.alpha];

            # subs
            if subnode.tag == 'subviews':
                for subv in subnode:
                    uiobject = find_ui_byid(subv.attrib.get('id'), ui_list)
                    v.subviews.append(uiobject)
                    uiobject.parent = v
            # cons
            if subnode.tag == 'constraints':
                for constraint in subnode.iter():
                    if  constraint.tag == 'constraint':
                        v.constraints.append(constraint)

        for c  in allconstraints:
                if c.attrib.get('firstItem') == v.id:
                    v.constraints.append(c)

        # print '*' * 100

        # print '\n'
    return ui_list

def gettype(v):
    vtype = ''
    try:
        vtype = 'UI' + toCap(v.type)
    except:
        vtype = 'normal'
    return vtype
def mas_method(firstItem,firstAttribute,secondItem,secondAttribute,multiplier,constant,relation):
    relation = 'mas_'+relation if relation else 'mas_equalTo'

    # filetypelist = ['Cell', 'View', 'ViewController']
    if  not (secondItem and secondAttribute) or  find_ui_byid(secondItem, uis)== None:
        if file_type == 'Cell':
            secondItem = 'self'
            secondAttribute = 'contentView'

        if file_type == 'View':
            secondItem = 'self'
            secondAttribute = ''

        if file_type == 'ViewController':
            secondItem = 'self'
            secondAttribute = 'view'
    else:
        secondItem = 'self.'+find_ui_byid(secondItem, uis).name
        secondAttribute = 'mas_'+secondAttribute

    s = '\t\tmake.${firstAttribute}.${relation}(${secondItem}.${secondAttribute}).mas_offset(${constant}).multipliedBy(${multiplier})'
    s  =  string.Template(s).safe_substitute({'firstAttribute': firstAttribute,
                                              'relation': relation,
                                              'secondItem':secondItem,
                                              'secondAttribute':secondAttribute,
                                              'constant':constant,
                                              'multiplier': multiplier,
                                              })

    return  s.replace('.multipliedBy(None)','').replace('.mas_offset(None)','')+';\n'

def gen_mas(v):

    if len(v.constraints) == 0:return ''

    layout = ''
    for constraint in set(v.constraints):
        cons_obj = my(constraint.attrib)
        layout += mas_method(cons_obj.firstItem, cons_obj.firstAttribute, cons_obj.secondItem, cons_obj.secondAttribute, cons_obj.multiplier,  cons_obj.constant, cons_obj.relation)

    s = '''
     [self.${name} mas_makeConstraints: ^ (MASConstraintMaker * make){
${layout}
     }];
    '''
    return string.Template(s).safe_substitute({'name':v.name,'layout':layout})

def gen_getter(v):
    if v is None: return ''
    name = v.name
    vtype = 'UI'+toCap(v.type)
    props_set = tab(v.getProp_set(),2)

    s = '''
- (${type} *)${name}{

    if (!_${name})
    {
        _${name} = [[${type} alloc] init];
    ${props_set}
    }
    return _${name};
}
        '''
    s = string.Template(s).safe_substitute({'name':name,'type':vtype,'props_set':props_set})

    return s



def gen_xib_file(f):

    global uis, file_type
    root = get_root(f)
    uis = parse(root)
    file_type = find_type(root)
    rfile = ''
    if file_type == 'Cell':
        rfile = 'cell.html'
    elif file_type == 'ViewController':
        rfile = 'c.html'
    else:
        rfile = 'v.html'
    for ui in uis:
        if 'CellContentView' in ui.name and file_type == 'Cell':
            ui.name = 'contentView'
            file_type == 'View'
    allSubUI = uis[2:] if file_type == 'Cell' else uis[1:]
    uiNames = map(lambda ui: 'UI' + toCap(ui.type) + ' ' + ui.name + '  ' + 'self.' + ui.parent.name, allSubUI[1:])
    render_getter = ''
    for x in ''.join(map(lambda v: gen_getter(v), allSubUI)).split('\n'):
        if len(x.strip()):
            for y in x.split('\n'):
                if len(y.strip()):
                    render_getter += y + '\n'
    render_mas = ''
    for x in ''.join(map(lambda v: gen_mas(v), allSubUI)).split('\n'):
        if len(x.strip()):
            # for y in x.split('\n'):
            #         if len(y.strip()):
            render_mas += x + '\n'
    render_subviews = ''
    for x in mvcTempleMaker.addSubViews(uiNames).split('\n'):
        if len(x.strip()):
            for y in x.split('\n'):
                if len(y.strip()):
                    if file_type == "Cell":
                        render_subviews += '\t' + y + '\n'

                    if file_type == "ViewController":
                        render_subviews += y + '\n'

                    if file_type == "View":
                        render_subviews += '\t' + y + '\n'
    filename = os.path.basename(f).split('.')[0]
    html = render_template(rfile, {'name': filename,
                                   'protocols': mvcTempleMaker.get_protocols(uiNames),
                                   'props': mvcTempleMaker.get_props_all(uiNames),
                                   'subviews': render_subviews,
                                   'buttons': map(lambda x: x, mvcTempleMaker.get_buttons(uiNames)),
                                   'hasProtocls': 'Table' in ''.join(mvcTempleMaker.get_protocols(uiNames)),
                                   'masornys': render_mas,
                                   'hasmas': True,
                                   'getters': render_getter
                                   })

    out_file = os.path.dirname(f)+'/'+filename + '1.m'
    with open(out_file, 'w') as rf:
        rf.write(html)
        os.system('open ' + out_file)




