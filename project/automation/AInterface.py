#encoding=utf-8
from ATool import wk
from ATool import Util
from ATool import mkmvc
from ATool import props
from ATool import getters
from ATool import sortcode
from ATool import xibparse
from ATool import folderUtil
from ATool import gen_hyb_xib
from ATool import jsontofield
from ATool import mvcTempleMaker
from ATool import MylayoutXibParse
from ATool.Util import simulate
from ATool.Util import readlines_from_stdin

def sort():
    sortcode.sortcode()

def mkdirs():
    map(folderUtil.mkdirs, set(Util.readlines_from_stdin()))

def output_props():
    lines = readlines_from_stdin()
    props.output_props(lines)

def output_getter():
    getters.out_getters()

def output_props_getters():
    lines = readlines_from_stdin()
    props.output_props(lines)
    getters.out_getters(lines)

def output_json2field():
    jsontofield.output_json2field()

def output_mvc():
    mkmvc.output_mvc()

#---------- xib 链式
def output_temple_type(mtype):
    mvcTempleMaker.output_type(mtype)  #c,v,cell

def output_xib():
    map(xibparse.gen_xib_file,Util.readlines_from_stdin())

def gen_mylayout():
    map(MylayoutXibParse.gen_xib_file,Util.readlines_from_stdin())


#useless
def hidden_folder():
    map(folderUtil.hidden_folder, set(Util.readlines_from_stdin()))

def show_folder():
    map(folderUtil.show_folder, set(Util.readlines_from_stdin()))

def showAll():
    folderUtil.showAll()

def hiddenAll():
    folderUtil.hiddenAll()
# simulate(u'/Users/liubo/Downloads/RollingView/RollingView/fdsView.xib')
# gen_hyb()




