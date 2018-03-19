from ATool import sortcode
from ATool import Util
from ATool import folderUtil
from ATool import getters
from ATool import props
from ATool import jsontofield
from ATool import mkmvc
from ATool import mvcTempleMaker
from ATool import xibparse
from ATool import wk


def sort():
    sortcode.sortcode()

def hidden_folder():
    map(folderUtil.hidden_folder, set(Util.readlines_from_stdin()))

def show_folder():
    map(folderUtil.show_folder, set(Util.readlines_from_stdin()))

def showAll():
    folderUtil.showAll()

def hiddenAll():
    folderUtil.hiddenAll()

def mkdirs():
    map(folderUtil.mkdirs, set(Util.readlines_from_stdin()))

def output_getter():
    getters.out_getters()

def output_props():
    props.output_props()

def output_json2field():
    jsontofield.output_json2field()

def output_temple_type(mtype):
    mvcTempleMaker.output_type(mtype)  #c,v,cell

#=======
def output_mvc():
    mkmvc.output_mvc()

def output_xib():
    map(xibparse.gen_xib_file,Util.readlines_from_stdin())

def rename_file(f,old,new):
	wk.traverse(f,old,new)


# f = '/Users/liubo/Documents/nib/automatic/automatic/sssTableViewCell.xib'
# f = '/Users/liubo/Documents/nib/automatic/automatic/fsViewController.xib'
# f = '/Users/liubo/Documents/nib/automatic/automatic/qqqView.xib'




