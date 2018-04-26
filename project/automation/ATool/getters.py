import re,os
from UI import UI
from  Util import *
import props

def gen_getter(rline):
    mtype = filter(lambda x: len(x), re.split(r'[;,\s ]\s*', rline))[2].replace('*', '')
    name = filter(lambda x: len(x), re.split(r'[;,\s ]\s*', rline))[3].replace('*', '')
    typefile = myLow(mtype.replace('UI', ''))

    try:
        html = render_template('custom' + '.html', {'name': name,'type':mtype,'all':render_template(typefile + '.html', {'name': name,'ui':UI()})})
        return  '\n'.join(filter(lambda x:len(x),html.split('\n'))).replace('@"None"','<#value#>').replace('None','<#value#>').replace('CGRectMake(0,0,0,0)','CGRectMake(<#x#>,<#y#>,<#w#>,<#h#>)')
    except:
        return render_template('custom' + '.html', {'name': name,'type':mtype})


def out_getters(lines = []):
    l = []
    if len(lines) == 0:
        l = readlines_from_stdin()
    else:
        l = lines

    if len(filter(lambda line: '@property' in line, l)):
        for line in l:
            print line

    for line in l:
        if line.startswith('/'):
            print line
        elif '@property' in line:
            gen_getter(line)
        else:
            for rline in props.getProps(line):
                print gen_getter(rline)