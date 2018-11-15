---
iOS代码自动化工具
---
一直以来都想写个自动化的工具，简化iOS开发，自动化脚本主要有以下几种方式：
``` bash
commandline:这种方式利用命令行执行生成代码，但是每次都要打开命令行，cd到目录，然后执行，传参数，不是特方便
Xcode插件，苹果屏蔽了好多很好用的插件，很怀恋自动显示图片的那个插件
图形化界面，做个图形化的界面点击生成代码，嗯，这倒是个不错的好主意
workflow，目前可以支持Python，Ruby，shell等脚本语言，利用自己喜欢的语言实现插件功能，我要讲的就是这个
结合我写的基础mvc架构，工程在这里（https://github.com/liubobo/AMBaseProject），便可以大批量生产代码
```

## 安装方式
``` bash
git clone https://github.com/liubobo/automation.git
cd automation/project && sudo /usr/bin/python setup.py develop&&sudo python setup.py develop
点击安装Services下的workflow

注：
如果喜欢写链式代码的可以安装chain目录下的代码，这个需要完善，实例可以看这里
https://github.com/liubobo/chain
```


## 本文主要教workflow这种方式，一图胜千言， Let's start!
``` bash
新建一个workflow，选择命令行，然后选你喜欢的语言，这里我选的是Python，
位于选项选Xcode,表示可以在Xcode右键执行代码
输出内容替换文本选项则是选的文字会被脚本输出代替，
服务收到选项 选文本表示可以获取文字内容，选文件夹，文件则可以获取文件路径
保存后系统会在 ~/Library/Services 路径下生成workflow

苹果在macos 10.14改变了这个新建选项，变成了快速操作选项
```
![](iOS自动化/start.gif)

## 排序功能，会对多行文字按照长短来排序，可以排列头文件，或是排列的代码块,默认会按照字母排列，如果已经排好了，会按照长度排列
![](iOS自动化/sort.gif)

## automation_view 会根据xcode中第一行来生成View的类名，下面的几个按照UI控件的类型来各自生成相应的UI代码
命名的时候要规范，指定是Button或Label等
![](iOS自动化/view.gif)

## automation_cell 会根据xcode中第一行来生成Cell的类名,下面生成模板代码
![](iOS自动化/cell.gif)

## automation_vc 会根据xcode中第一行来生成VC的类名,下面生成模板代码,事件，代理，方法等
![](iOS自动化/vc.gif)

## automation_prop 功能可以生成属性代码
![](iOS自动化/prop.gif)

## automation_getter 功能可以生成getter代码
![](iOS自动化/getter.gif)

## automation_hidden 功能可以生成隐藏文件或文件夹，这个我打算去掉，感觉用处不大

![](iOS自动化/sh.gif)

## automation_mvc 功能可以根据文件夹批量生成文件夹mvc代码，（https://github.com/liubobo/AMBaseProject）
## 如果想自定义模板可以改相关代码
![](iOS自动化/mvc.gif)

## automation_json2model 功能可以根据json来生成相应的属性代码，LoginModel的实现文件里面有个默认模板
是根据自己的架构设计而来，需要修改的可以在templates目录改模板内容
![](iOS自动化/json2model.gif)

## automation_mkfolders 批量创建文件夹
![](iOS自动化/mkfolders.gif)

## automation_xib2file  可以把xib转化为代码文件，默认布局为masorny代码,在Document的Label标签下可以给控件起名字
![](iOS自动化/xib2file.gif)

持续完善中，如有bug，issue，或是还有可以自动化的地方可以联系我
qq 602318557




