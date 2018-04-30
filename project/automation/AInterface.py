#encoding=utf-8
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
from ATool.Util import readlines_from_stdin
from ATool.Util import simulate
from ATool import gen_hyb_xib

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
    lines = readlines_from_stdin()
    props.output_props(lines)

def output_props_getters():
    lines = readlines_from_stdin()
    props.output_props(lines)
    getters.out_getters(lines)

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

def gen_hyb():
    map(gen_hyb_xib.gen_xib_file,Util.readlines_from_stdin())

# simulate(u'/Users/liubo/Downloads/RollingView/RollingView/fdsView.xib')
# gen_hyb()




