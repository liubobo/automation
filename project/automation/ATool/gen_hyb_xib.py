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
    for cell in root.iter("tableViewCell"): # cell
        if cell is not None:
            return 'Cell'
    for country in root.iter("placeholder"): #vc
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
            arr = filter(lambda v: v.id == v_id, ui_list)
            if len(arr):
                v = arr[0]
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
        print  node.tag
        print '*' * 100

        v = find_ui_byid(node.attrib.get('id'), ui_list)
        for subnode in node:
            if subnode is None:continue
            # print subnode.tag
            if subnode.tag == 'rect':
                rect = my(subnode.attrib)
                v.frame = 'CGRectMake('+','.join([rect.x,rect.y,rect.width,rect.height])+')'
                print  v.frame

            if subnode.tag == 'color':
                color = my(subnode.attrib)
                v.backgroundColor = [color.green,color.red,color.blue,color.alpha];
                print v.backgroundColor

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

        print '*' * 100

        print '\n'
    print_obj(ui_list)

    return ui_list

def gettype(v):
    vtype = ''
    try:
        vtype = 'UI' + toCap(v.type)
    except:
        vtype = 'normal'
    return vtype

def hyb_addSubviews(myUIS):

    result = ''
    for x in myUIS:
        parent = x.parent.name
        if parent == 'view':
            parent = 'self.view'
        tp = ''
        ls = ['view','button','label','imageView','textField','tableView'];
        if x not in ls:
                    tp =   '''
    _$name = [''' + '''UI'''+toCap(x.type)+''' km_makeView: ^ (KMUIViewMaker * make){
                make.frame($frame).backgroundColor([UIColor ]).addToSuperView(
                    $pa).addMasorny( ^ (MASConstraintMaker * maker){
                    });
    }];'''


        if x.type == 'view':
            tp =   '''
    _$name = [UIView km_makeView: ^ (KMUIViewMaker * make){
                make.frame($frame).backgroundColor([UIColor ]).addToSuperView(
                    $pa).addMasorny( ^ (MASConstraintMaker * maker){
                    });
    }];'''

        if x.type == 'button':
            tp = '''
    _$name = [UIButton km_makeButton:^(KMButtonMaker *make) {
                  make.titleForState(@"", UIControlStateNormal).addTargetAndActionForControlEvents(self, @selector($name ButtonTouchUpInside), UIControlEventTouchUpInside).imageForState([UIImage imageNamed:@""], UIControlStateNormal).titleColorForState([UIColor redColor], UIControlStateNormal).backgroundColor([UIColor redColor]).frame(CGRectMake(0, 0, 0, 0)).tag(0).addToSuperView(nil).addMasorny(^(MASConstraintMaker *maker){

    });}];
                  
                  '''

        if x.type == 'label':
            tp = '''
   _$name = [UILabel km_makeLabel:^(KMLabelMaker *make) {
        make.text(@"").textAlignment(NSTextAlignmentLeft).font(nil).tintColor(nil).frame(CGRectMake(0, 0, 0, 0)).addMasorny(^(MASConstraintMaker *maker){

        });
    }];
                '''


        if x.type == 'imageView':
            tp = '''
   _$name =  [UIImageView km_makeImageView:^(KMImageViewMaker *make) {
        make.image(nil).backgroundColor(nil).frame(CGRectMake(0, 0, 0, 0)).addToSuperView(self.view).addMasorny(^(MASConstraintMaker *maker){

         });
    }];
    '''


        if x.type == 'textField':
            tp = '''
    _$name = [UITextField km_makeTextField:^(KMTextFieldMaker *make) {
        make.placeholder(nil).textColor(nil).font(nil).frame(CGRectMake(0, 0, 0, 0)).addToSuperView(self.view).addMasorny(^(MASConstraintMaker *maker){
                        
         });
    }];'''


        if x.type == 'tableView':
            tp = '''
   _$name =  [UITableView km_makeTableViewWithStyle:UITableViewStylePlain block:^(KMTableViewMaker *make) {
        make.frame(CGRectMake(0, 0, 0, 0));
    }];'''

        result += string.Template(tp).safe_substitute({'frame': x.frame,'pa':parent,'name':x.name})


    return result


def gen_xib_file(f):

    global uis, file_type
    root = get_root(f)
    uis = parse(root)
    file_type = find_type(root)
    rfile = ''
    if file_type == 'Cell':
        rfile = 'hycell.html'
    elif file_type == 'ViewController':
        rfile = 'hyc.html'
    else:
        rfile = 'hyv.html'
    for ui in uis:
        if 'CellContentView' in ui.name and file_type == 'Cell':
            ui.name = 'contentView'
            file_type == 'View'

    allSubUI = uis[2:] if file_type == 'Cell' else uis[1:]
    uiNames = map(lambda ui: 'UI' + toCap(ui.type) + ' ' + ui.name + '  ' + 'self.' + ui.parent.name, allSubUI[0:])
    subs = hyb_addSubviews(allSubUI)

    filename = os.path.basename(f).split('.')[0]
    html = render_template(rfile, {'name': filename,
                                   'hyb_addSubviews':subs,
                                   'protocols': mvcTempleMaker.get_protocols(uiNames),
                                   'props': mvcTempleMaker.get_props_all(uiNames),
                                   'buttons': map(lambda x: x, mvcTempleMaker.get_buttons(uiNames)),
                                   'hasProtocls': 'Table' in ''.join(mvcTempleMaker.get_protocols(uiNames)),
                                   })

    out_file = os.path.dirname(f)+'/'+filename + '1.m'
    with open(out_file, 'w') as rf:
        rf.write(html)
        os.system('open ' + out_file)




