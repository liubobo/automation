from viewList import vList
from myIo import *
from ui import UI

def gen_ui(line):
    line = line.replace(';','')
    ui = UI()

    if ')' in  line:
        line = line.split(')')[1]
        ui.isProp = True

    ui.type =  line.replace(' ','').split('*')[0]
    ui.name =  line.replace(' ','').split('*')[1]

    return ui

def gen_uis():
    return  map(gen_ui, readlines_from_stdin())

