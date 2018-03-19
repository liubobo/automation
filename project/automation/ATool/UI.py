import os
from  Util import *

from  mydict import MyDict as my

class UI(object):
    def __init__(self):
        self.frame = 'CGRectMake(0,0,0,0)'
        self.id = ''
        self.parent = 'self'
        self.name = ''
        self.masonry = ''
        self.customClass = None

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

        # print  self.mylayout
        if self.type == 'button':
            self.setButtonProps()

        if self.type == 'label':
            self.setLabelProps()

        if self.type == 'imageView':
            self.setImageViewProps()

        if self.type == 'tableView':
            print  ''#self.props
        try:
            return  render_template(self.type+'.html',{'name':self.name,'ui':self})
        except:
            with open('./templates/'+self.type+'.html','w') as f:
                f.write('_{{name}}.frame = {{ ui.frame }};')

        return render_template('normal_ui.html', {'name': self.name, 'ui': self})


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