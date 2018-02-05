#coding=utf-8
from util import *
import xml.etree.ElementTree as etree
from  mydict import MyDict as my

def getname(v):
    vName = v.name if hasattr(v, 'name') else v.props.id + '_'
    return vName + myCap(v.tag)

def getPops(v):
    vType = 'UI' + myCap(v.tag)
    if v.tag == 'tableViewCellContentView':
        return ''
    return '@property (nonatomic, strong) ' + vType + '  *' + getname(v) + ';'

def buttonTouchs(v):
  if not hasattr(v, 'isRoot') and v.tag == 'button':
      return '- (void)' + getname(v) + '''ButtonTouchUpInside:(UIButton *)sender\n{\n}'''
  else:
      return ''

def get_constraint_value(attrib,k):
  if attrib.get(k):
      return attrib.get(k)
  if k == 'constant':
      return '0'
  return ''

def openTemple(html,path):
  name = os.path.basename(path).split('.')[0]
  file1 = os.path.dirname(path)+'/'+name+'1.m'
  with open(file1,'w') as f:
      f.write(html)
      os.system('open '+file1)

def genfile(path):

  viewlist = []
  namelist = []
  filetypelist = ['Cell','View','ViewController']
  xibName = os.path.basename(path).split('.')[0]

  fileType = filter(lambda x:xibName.endswith(x),filetypelist)[0]
  vList = ['activityIndicatorView','pageControl','tableViewCellContentView',"view","label","textField","textView","button","imageView","switch","tableView","scrollView",'segmentedControl']

  tree = etree.parse(path)
  root = tree.getroot()

  #find all views
  for child in root.iter():
      if child.tag in vList:
          child.props = my(child.attrib)
          child.subviews = []
          viewlist.append(child)
  #parse outlets names
      if child.tag == 'placeholder':
          if child.attrib['placeholderIdentifier'] == 'IBFilesOwner':
              for outLets in child.iter():
                  if outLets.attrib.get('property'):
                      namelist.append(outLets)

  rootView = viewlist[0]
  rootView.isRoot = True

  for view in viewlist:
      view.constraints = []
      for name in namelist:
          if view.props.id == name.attrib.get('destination'):
              view.name = name.attrib.get('property')
      if view.tag in vList:
         for child in view.iter():  # subviews
           if child.tag in vList:
               if child.attrib['id'] != view.props.id:
                  view.subviews.append(child)
                  child.parent = view
           elif child.tag == 'rect':
                  view.rect = my(child.attrib)
           elif child.tag == 'connections':
               view.event = my(child.attrib)
               for sun in child:
                   view.event = my(sun.attrib)
           elif child.tag == 'constraints':
               for constraint in child:
                   constraint.father = view
                   view.constraints.append(constraint)

  print 'begin temple render'.center(100,'*')
  subview_list = viewlist[1:]

  def layoutSubViews(v):
      if not hasattr(v,'isRoot'):
          parentView = 'self.' + getname(v.parent)
          if hasattr(v.parent,'isRoot'):
              parentView = 'self'
              if fileType == 'cell':
                  parentView = 'self.contentView'
              parentView  = 'self.view' if fileType=='ViewController' else 'self'
          return '['+parentView +' addSubview:'+'self'+'.' + getname(v)+']'
      else:
          return ''

  def findConstraintsById(mid):
      return filter(lambda constraint:get_constraint_value(constraint.attrib,'firstItem') == mid,viewlist[0].constraints)

  for view in subview_list:
          view.constraints.extend(findConstraintsById(view.attrib['id']))

  def findViewById(id):
      for view in subview_list:
          if view.props.id == id:
              return getname(view)
      return ''

  masonrys = reduce(lambda x,y:x+y,map(lambda view:gen_mas(findViewById, view,fileType),subview_list))
  buttons, getters = gen_events(map(lambda v:getname(v), subview_list),subview_list)

  html = render_template('result'+'.m',
             {'props':'\n'.join(map(getPops, subview_list)),
             'layoutSubViews':'\n'.join(map(layoutSubViews, viewlist)),
             'touches':'\n'.join([x  for x in  map(buttonTouchs, viewlist) if len(x)])+'\n',
             'masonrys':masonrys,
             'sums':getters
             })

  openTemple(html,path)

#mas firstItem.firstAttribute {==,<=,>=} secondItem.secondAttribute * multiplier + constant
def gen_mas(findViewById, view, fileType):


    result = ''
    result += "[self." + getname(view) + ''' mas_makeConstraints: ^ (MASConstraintMaker * make){''' + '\n'

    for constraint in view.constraints:
        relation = get_constraint_value(constraint.attrib, 'relation')
        if not relation:
            relation = 'equalTo'
        secondItem = get_constraint_value(constraint.attrib, 'secondItem')
        firstAttribute = get_constraint_value(constraint.attrib, 'firstAttribute')
        secondAttribute = get_constraint_value(constraint.attrib, 'secondAttribute')
        constant = get_constraint_value(constraint.attrib, 'constant')
        multiplier = get_constraint_value(constraint.attrib, 'multiplier')
        v_parent = 'self.view' if fileType == 'ViewController' else 'self'

        if secondItem:
            v_parent = 'self'
            if findViewById(secondItem):
                result += '\t' + 'make.' + firstAttribute+ '.mas_'+relation +'(' + v_parent +'.' + findViewById(secondItem) + '.' + secondAttribute + ')' + '.offset(' + constant + ')'
            else:
                result += '\t' + 'make.' + firstAttribute + '.mas_'+relation+'(' + v_parent + ')' + '.offset(' + constant + ')'
        else:
            result += '\t' + 'make.' + firstAttribute + ".mas_"+relation+"(" + constant + ")"
        if multiplier:
            result += '.multipliedBy('+str(multiplier)+')'
        result+=';\n'

    result += '\n' + "}];\n"
    return result
# simulate(u'/Users/liubo/Desktop/代码工具/UINibParser-master-3/UINibParser/TestUIViewViewController.xib')
map(genfile,set(map(lambda line:str(line).strip('\n').strip(' '),readlines_from_stdin())))



