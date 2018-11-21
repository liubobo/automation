#coding:utf8
import json
import viewLists
import Util,string
from  mydict import MyDict as my
import xml.etree.ElementTree as etree
import os

f_type = 'vc'

def gen_xib_file(file_path):
    f = open(file_path,'r')

    tree = etree.parse(file_path)
    root = tree.getroot()
    root_node_id = None
    ui_list = []

    def is_ui_node(node):
        for x in node:
            if x.tag == 'rect':
                return [x.attrib.get('x'),x.attrib.get('y'),x.attrib.get('width'),x.attrib.get('height')]
        return []

    def ui_type(node):
        return 'UI'+Util.toCap(node.tag)

    def ui_name(node):
        ui_type = Util.toCap(node.tag)
        if node.attrib.get('id') == root_node_id:return 'view'

        if node.attrib.get('userLabel'):
            return node.attrib.get('userLabel')+ui_type
        else:
            return node.attrib.get('id')+ui_type

    def is_ui_father(node):
        for x in node:
            if x.tag == 'subviews':
                return True
        return False

    def file_type():
        global f_type
        if root_node_id == 'iN0-l3-epB':
            f_type = 'view'

        if root_node_id == 'H2p-sc-9uM':
            f_type = 'cell'
        return f_type

    #need for output
    def gen_prop(node):
        if node.attrib.get('id') == root_node_id:return ''
        return '@property(nonatomic, strong) '+ui_type(node)+'*'+ ui_name(node)+';'

    def gen_add(node):
        if is_ui_father(node):
            l = ''
            for x in node:
                 if x.tag == 'subviews':
                     for y in x:
                         l = l+('[self.'+ui_name(node) +' addSubview:self.'+ui_name(y)+'];'+'\n')
            if file_type() =='view':
                l = l.replace('self.view','self')
            if file_type() =='cell':
                l = l.replace('self.view','self.contentView')

            return l
        return ''

    def gen_event(node):
        if node.tag == 'button':
            return '- (void)'+ui_name(node)+'''TouchUpInside:(UIButton *)sender{	}'''
        return ''

    def gen_getter(node):
        if node.attrib.get('id') == root_node_id:return ''
        s =  '''- (${type} *)${name}{
        
        if (!_${name})
        {
            _${name} = [[${type} alloc] init];
        ${mylayout}
        }
        return _${name};
    }
        '''
        my_layout = gen_mylayout(node) if gen_mylayout(node) else ''
        return string.Template(s).safe_substitute({'type':ui_type(node),'name':ui_name(node),'mylayout':my_layout})


    def gen_mylayout(node):
        out_put = ''
        for x  in node:
            if x.tag == 'userDefinedRuntimeAttributes':
                for y in x:
                    if y.attrib.get('type')=='boolean':
                        out_put = out_put+ '_'+ui_name(node)+'.'+y.attrib.get('keyPath')+'='+y.attrib.get('value') +';\n'

                    if y.attrib.get('type') == 'number':
                        for z in y:
                            if z.tag == 'real':
                                out_put = out_put + '_' + ui_name(node) + '.' + y.attrib.get('keyPath') + '=' + z.attrib.get('value') + ';\n'

                    if y.attrib.get('type') == 'point':
                        for z in y:
                            if z.tag == 'point':

                                 out_put = out_put + '_' + ui_name(node) + '.' + y.attrib.get('keyPath') + '=' +'CGPointMake('  + z.attrib.get('x')+','+z.attrib.get('y')+')' + ';\n'

                return out_put


    class UIObj(object):
        def __init__(self,node):
            self.prop = gen_prop(node)
            self.add  = gen_add(node)
            self.event = gen_event(node)
            self.getter = gen_getter(node)

    for node in root.iter():
        rect_list = is_ui_node(node)
        is_ui =  len(rect_list)
        if not is_ui: continue
        if not root_node_id: root_node_id = node.attrib.get('id')
        ui = UIObj(node)
        ui_list.append(ui)

        gen_mylayout(node)



    file_name = os.path.splitext(os.path.basename(file_path))[0]
    html = Util.render_template('new_xib_parse.html', {'name': file_name,'uis':ui_list,'f_type':f_type})

    out_file = os.path.dirname(file_path) + '/' + file_name + '1.m'
    with open(out_file, 'w') as rf:
        rf.write(html)
        os.system('open ' + out_file)



# gen_xib_file(u'/Users/hc/Desktop/HengYiBao的副本/ViewController.xib')