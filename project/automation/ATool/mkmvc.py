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
//
//  Created by liubo on 2017/12/21.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HYBModel.h"

@interface ${name}Model : HYBModel

 

@end

'''

mTemplem = '''
//
//  ${name}Model.m
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
//
//  Created by liubo on 2017/12/22.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import "HYBView.h"

@interface ${name}View : HYBView


@end


'''
vTemplem = '''

//
//  ${name}View.m
//
//  Created by liubo on 2017/12/22.
//  Copyright © 2017年 liubo. All rights reserved.
//

#import "${name}View.h"

@implementation ${name}View

- (void)hyb_setupViews {

}


@end

'''

cTempleh = '''
//
//  ${name}ViewController.h
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
//
//  Created by liubo on 2018/2/1.
//  Copyright © 2018年 liubo. All rights reserved.
//

#import "${name}ViewController.h"

@interface ${name}ViewController ()

@end

@implementation ${name}ViewController

#pragma mark - Life Cycle Methods

#pragma mark - Override Methods
//1.设置导航
- (void)hyb_layoutNavigation {
}

//2.初始化数据
- (void)hyb_setUpData {

}

//3.摆放view
- (void)hyb_addSubviews {

}

//4.获取新数据刷新
- (void)hyb_getNewData {
}
#pragma mark - Intial Methods

#pragma mark - Network Methods

#pragma mark - event Methods

#pragma mark - Public Methods

#pragma mark - Private Methods

#pragma mark - UITableViewDataSource
#pragma mark - UITableViewDelegate

#pragma mark - delegate

#pragma mark - Lazy Loads


@end

'''