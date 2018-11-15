#coding=utf-8
import os,sys,string
from Util import *

def genDir(path):

   	name  = os.path.basename(path)
	dirs = os.path.dirname(path)+'/'+name+'/'
	
	dic	 = {
		    	'Model':[mTempleh,mTemplem],
		    	'View' :[vTempleh,vTemplem],
		    	'ViewController':[cTempleh,cTemplem]
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
//  Created by 自定义 on 2017/12/21.
//  Copyright © 2017年 自定义. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "AMModel.h"

@interface ${name}Model : AMModel

 

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

- (AMHttp)method {
        return AMHttpPost;
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

#import "AMView.h"

@interface ${name}View : AMView


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

- (void)am_setupViews {

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


@interface ${name}ViewController : UIViewController 

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
- (void)am_layoutNavigation {
}

//2.初始化数据
- (void)am_setUpData {

}

//3.摆放view
- (void)am_addSubviews {

}

//4.获取新数据刷新
- (void)am_getNewData {
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