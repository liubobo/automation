# coding: utf-8
from core.myIo import *
import string,os
from core import UIReform
import sys
reload(sys)

sys.setdefaultencoding('utf8')

# simulate(u'uibutton *bb;\nuibutton *bb\nuibutton *bb\nuibutton *bb\n@property (nonatomic, strong) UIButton *bxx;')

# simulate(u' UIButton *v')

for ui in   UIReform.gen_uis():

    ui_type = ui.type+ '*' if not ui.isProp  else ''

    if ui.type == 'UIButton':
        s = ''' 
        ${mtype}${name} = [UIButton km_makeButton:^(KMButtonMaker *make) {

        make.titleForState(@"", UIControlStateNormal).textFont(kFont15).addTargetAndActionForControlEvents(self, @selector(${tname}ButtonTouchUpInside:), UIControlEventTouchUpInside).frame(CGRectMake(0, 0, 0, 0)).backgroundColor([UIColor redColor]).addToSuperView(<#(nonnull UIView *)#>).addMasorny(^(MASConstraintMaker *maker) {

        });
        }];
        '''
        s = string.Template(s).safe_substitute({'name': '_'+ui.name if ui.isProp else ui.name,'tname':ui.name,'mtype':ui_type})


    elif  ui.type == 'UILabel':
        s = '''
        ${mtype}${name} = [UILabel km_makeLabel:^(KMLabelMaker *make){
        
        make.font(kFont15).tintColor([UIColor redColor]).frame(<#CGRect frame#>).addToSuperView(<#UIView *superView#>);

    }];
              '''
        s = string.Template(s).safe_substitute(
            {'name': '_' + ui.name if ui.isProp else ui.name, 'tname': ui.name, 'type': ui.type,'mtype':ui_type})


    elif ui.type == 'UIImageView':
        s = '''  ${mtype}${name} = [UIImageView km_makeImageView: ^ (KMImageViewMaker * make)
        {
            make.image( <#UIImage *image#>).frame(<#CGRect frame#>).addToSuperView(<#UIView *superView#>);;
        }];
                   '''
        s = string.Template(s).safe_substitute(
            {'name': '_' + ui.name if ui.isProp else ui.name, 'tname': ui.name, 'type': ui.type,'mtype':ui_type})

    else:
        s = '''
         ${mtype}${name}  = [ ${type} km_makeView:^(KMUIViewMaker *make) {
          make.frame(CGRectMake(<#CGFloat x#>, <#CGFloat y#>, <#CGFloat width#>, <#CGFloat height#>)).backgroundColor([UIColor redColor]).addToSuperView(<#(nonnull UIView *)#>);
        }];
        '''
        s = string.Template(s).safe_substitute({'name': '_'+ui.name if ui.isProp else ui.name,'tname':ui.name,'type':ui.type,'mtype':ui_type})


    print s

