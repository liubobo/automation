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

如果喜欢写链式代码的可以安装chain目录下的代码，这个需要完善，实例可以看这里
https://github.com/liubobo/chain
```

## 教程
https://liubobo.github.io

持续完善中，如有bug，issue，或是还有可以自动化的地方可以联系我
qq 602318557




