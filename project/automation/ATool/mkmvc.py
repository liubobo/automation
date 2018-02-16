#coding=utf-8
import os,sys,string
from Util import *

def genDir(path):

   	name  = os.path.basename(path)
	dirs = os.path.dirname(path)+'/'+name+'/'
	
	dic	 = {
		    	'Model':[mTempleh,mTemplem],
		    	'View' :[vTempleh,vTemplem],
		    	'Controller':[cTempleh,cTemplem]
		    }

	for k,v in dic.items():
		os.makedirs(dirs+k)		
		with open(dirs+k+'/'+name+k+'.h','w') as f:
			f.write(string.Template(v[0]).safe_substitute({'name':name}))
	 
		with open(dirs+k+'/'+name+k+'.m','w') as f:
			f.write(string.Template(v[1]).safe_substitute({'name':name}))


def output_mvc():

	lines = set(readlines_from_stdin())
	map(genDir,lines)



















mTempleh = '''
//
//  HYLoginModel.h
//  BaiBaoBox
//
//  Created by liubo on 2017/12/21.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HYBModel.h"

@interface ${name}Model : HYBModel

@property(nonatomic, strong) NSString *name;
@property(nonatomic, strong) NSString *pwd;

@property(nonatomic, strong) NSString *info;

@end

'''

mTemplem = '''
//
//  ${name}Model.m
//  BaiBaoBox
//
//  Created by liubo on 2017/12/21.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import "${name}Model.h"

@implementation ${name}Model

- (NSString *)protocolUrl {
        return requestUrl(@"<#host#>", @"<#ver#>", @"<#path#>");
    }

    - (HYBHttp)method {
        return HYBHttp<#method#>;
    }

    - (NSString *)description {
        return @"<#接口描述#>";
    }

@end

'''

vTempleh = '''
//
//  DemoView.h
//  HengYiBao
//
//  Created by liubo on 2017/12/22.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import "HYBView.h"
#import "HYBRegisterViewModel.h"

@interface ${name}View : HYBView

@property(nonatomic, strong) HYBRegisterViewModel *viewModel;

@end


'''
vTemplem = '''

//
//  ${name}View.m
//  HengYiBao
//
//  Created by liubo on 2017/12/22.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import "${name}View.h"

@implementation ${name}View

- (instancetype)initWithViewModel:(id<HYBViewModelProtocol>)viewModel {
    self.viewModel = (HYBRegisterViewModel *)viewModel;
    return [super initWithViewModel:viewModel];
}

//如果数据变化，需要刷新视图的话，可以在这里监听
- (void)hyb_bindViewModel {

}

- (void)hyb_setupViews {

}


@end

'''

cTempleh = '''
//
//  ${name}ViewController.h
//  HengYiBao
//
//  Created by liubo on 2018/2/1.
//  Copyright © 2018年 liubo. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "HYBViewControllerProtocol.h"
#import "UIViewController+UIDefultUIStyle.h"

@interface ${name}ViewController : UIViewController <HYBViewControllerProtocol, HYBDefualtStyleUIProtocol>

@end

'''

cTemplem = '''
//
//  ${name}ViewController.m
//  HengYiBao
//
//  Created by liubo on 2018/2/1.
//  Copyright © 2018年 liubo. All rights reserved.
//

#import "${name}ViewController.h"

@interface ${name}ViewController ()

@end

@implementation ${name}ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
 #pragma mark - Navigation

 // In a storyboard-based application, you will often want to do a little preparation before navigation
 - (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
 // Get the new view controller using [segue destinationViewController].
 // Pass the selected object to the new view controller.
 }
 */

@end

'''