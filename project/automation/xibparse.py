#encoding=utf-8
from  tools import *
import os,sys,string
from  mydict import MyDict as my
import xml.etree.ElementTree as etree
from  viewLists import  vList as availables
class UI(object):
    def __init__(self):
        self.frame = 'CGRectMake(0,0,0,0)'
        self.id = ''
        self.parent = ''
        self.name = ''
        self.masonry = ''

        self.type = ''
        self.uselabel = ''
        self.props = None

        self.backgroundColor = []
        self.titleColor = None
        self.title = None
        self.image = None
        self.backgroundImage = None

        self.subviews = []
        self.parent = None
        self.constraints = []
        self.props_set = ''
        self.fontSize = ''

        self.mylayout = ''

    def getProp_set(self):
        for node in self.props.iter():

                if node.tag == 'userDefinedRuntimeAttributes':
                    for mynode in node:
                        try:
                            self.mylayout += self.name +'.'+ my(node.attrib).keyPath +'='+ my(mynode.attrib).value+';\n'
                        except:
                            try:
                                self.mylayout +=  self.name +'.'+ my(node.attrib).keyPath +'='+ my(node.attrib).value+';\n'
                            except:
                                if my(node.attrib).keyPath == 'mySize':
                                    self.mylayout +=  self.name +'.'+my(node.attrib).keyPath +'CGSizeMake('+my(mynode.attrib).width+my(mynode.attrib).height+');\n'

                                if my(node.attrib).keyPath == 'myCenter':
                                    self.mylayout += self.name +'.'+ my(node.attrib).keyPath +' =  CGPointMake('+ my(mynode.attrib).x +','+ my(mynode.attrib).y+');\n'
                                else:
                                    print ''
        print  self.mylayout
        if self.type == 'button':
            self.setButtonProps()

        if self.type == 'label':
            self.setLabelProps()

        if self.type == 'imageView':
            self.setImageViewProps()

        if self.type == 'tableView':
            print  self.props
        try:
            return  render_template(self.type+'.html',{'name':self.name,'ui':self})
        except:
            with open('./uis/'+self.type+'.html','w') as f:
                f.write('_{{name}}.frame = {{ ui.frame }};')

        return render_template('normal_ui.html', {'name': self.name, 'ui': self})

    def setMaylayout(self):
        pass


    def setImageViewProps(self):
        self.image = my(self.props.attrib).image if my(self.props.attrib).image else ''
    def setLabelProps(self):
        self.title = my(self.props.attrib).text
        self.numberOfLines = my(self.props.attrib).numberOfLines if my(self.props.attrib).numberOfLines else 0
        for node in self.props.iter():
            if node.tag == 'fontDescription':
                self.fontSize = my(node.attrib).pointSize
    def setButtonProps(self):
        for node in self.props.iter():
            if node.tag == 'state':
                self.title = my(node.attrib).title
                self.image = my(node.attrib).image
                self.backgroundImage = my(node.attrib).backgroundImage
                for color in node:
                    if color.tag == 'color':
                        self.titleColor = 'kColor<##>'

class RenderObject(object):

    def __init__(self):
        self.props = ''
        self.layoutSubViews = ''
        self.touches = ''
        self.masonrys = ''
        self.sums = ''
        self.file = ''
        self.delegates = ''
def get_root(file_path):
    file_type = get_filetype(file_path)
    tree = etree.parse(file_path)
    root = tree.getroot()
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
def parse(file_path):
    root = get_root(file_path)
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
f = '/Users/liubo/Desktop/代码工具/MyLinearLayout-master/MyLayoutDemo/Base.lproj/FLLTest2ViewController.xib'
uis = parse(f)
def gettype(v):
    vtype = ''
    try:
        vtype = 'UI' + toCap(v.type)
    except:
        vtype = 'normal'
    return vtype
def is_ui(v):
    vtype = gettype(v)
    return vtype in availables
def gen_property(v):
    vtype = gettype(v)
    if vtype in availables:
        return  '@property(nonatomic, strong) {} *{};'.format(vtype,v.name)
    else:
        return  '@property(nonatomic, strong) {} *{};'.format('<#type#>',v)
def gen_layout(v):
    if v.parent is None and get_filetype(f) == 'Cell':
        return '\t[self.{} addSubview:self.{}];'.format('contentView', v.name)
    return '\t[self.{} addSubview:self.{}];'.format(v.parent.name,v.name)
def gen_event(v):
    if v.type == 'button':
         return  '- (void){}TouchUpInside:(UIButton *)sender'.format(v.name)+'{ \n}'
    return ''
def mas_method(firstItem,firstAttribute,secondItem,secondAttribute,multiplier,constant,relation):
    relation = 'mas_'+relation if relation else 'mas_equalTo'

    # filetypelist = ['Cell', 'View', 'ViewController']
    if  not (secondItem and secondAttribute) or  find_ui_byid(secondItem, uis)== None:
        if get_filetype(f) == 'Cell':
            secondItem = 'self'
            secondAttribute = 'contentView'

        if get_filetype(f) == 'View':
            secondItem = 'self'
            secondAttribute = ''

        if get_filetype(f) == 'ViewController':
            secondItem = 'self'
            secondAttribute = 'view'
    else:
        secondItem = 'self.'+find_ui_byid(secondItem, uis).name

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
    if not is_ui(v): return ''
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
    name = v.name if is_ui(v) else v
    vtype = gettype(v) if is_ui(v) else '<#type#>'
    props_set = v.getProp_set() if is_ui(v) else ''

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
    return string.Template(s).safe_substitute({'name':name,'type':vtype,'props_set':props_set})


r = RenderObject()
r.props = '\n'.join(map(lambda v:gen_property(v),uis[1:]))
r.layoutSubViews = '\n'.join(map(lambda v:gen_layout(v),uis[1:]))
r.touches = '\n\n'.join(map(lambda v:gen_event(v),filter(lambda x:x.type == 'button' ,uis[1:])))
r.masonrys = ''.join(map(lambda v:gen_mas(v),uis[1:]))
r.sums = '\n'.join(map(lambda v:gen_getter(v),uis[1:]))
r.file = 'masorny.m'
# r.file = 'frame.m'
# f.file = 'mylayout.m'


html = render_template(r.file,
                       {'props':r.props,
                        'layoutSubViews':r.layoutSubViews,
                        'touches':r.touches,
                        'masonrys':r.masonrys,
                        'sums':r.sums
                        })

print  html