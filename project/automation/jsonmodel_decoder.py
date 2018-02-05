#! /usr/bin/python
#coding:utf-8
import json
from sys import argv
import re

classList = {}
gClassName = ""
isShort = 1
mainClass=""

COLORS  = {
    "blue": "0;34m",
    "green": "0;32m",
    "cyan": "0;36m",
    "red": "0;31m",
    "purple": "0;35m",
    "brown": "0;33m",
    "yellow": "1;33m",
    "lred": "1;31m",
}

def print_color_string(string, color):
    print string

def capitalize(name):
    if len(name) == 0 :
        return name
    nameArray = name.split('_')
    result = ""
    for nameTemp in nameArray:
        result = result + nameTemp.capitalize()
    return result

def composeClassName(prefix, subfixKey):
    global gClassName
    global isShort
    if isShort == 1:
        return (gClassName + capitalize(subfixKey))
    else:
        return (prefix + capitalize(subfixKey))

def simpleTypeName(ktype):
    if ktype == "<type 'int'>" or  ktype == "<type 'float'>":
        return "NSNumber"
    elif ktype == "<type 'bool'>":
        return "BOOL"
    elif ktype == "<type 'str'>" or ktype == "<type 'unicode'>":
        return "NSString"
    return None


def iterItem(item,className):
    if not str(type(item)) == "<type 'dict'>" :
        print "item type is: " , type(item)
        return
    for k , v in item.items():
        tempType = str(type(v))
        if tempType == "<type 'list'>":
            if len(v) > 0:
                it = v[0]
                ittype = str(type(it))
                if ittype == "<type 'dict'>":
                    subname = composeClassName(className, k)
                    iterItem(it, subname)
        elif tempType == "<type 'dict'>":
            subname = composeClassName(className, k)
            iterItem(v,subname)
    printHeader(item,className)

def printHeader(item,className):
    t = str(type(item))
    if not  t == "<type 'dict'>" :
        print "error type: " , t
        print "item is  : " , item
        print "className is: " , className
        return None
    global classList
    varlist = {}
    protocols = []
    header = "@interface " + className + "Model" + " : NSObject\n"
    for k , v in item.items():
        ktype = str(type(v))
        pname = unicode(k)
        if ktype == "<type 'int'>" or  ktype == "<type 'float'>":
            header += "@property (nonatomic, strong) NSNumber *%s;\n" % (pname)
        elif ktype == "<type 'bool'>":
            header += "@property (nonatomic, assign) BOOL %s;\n" % (pname)
        elif ktype == "<type 'str'>" or ktype == "<type 'unicode'>":
            header += "@property (nonatomic, strong) NSString *%s;\n" % (pname)
        elif ktype == "<type 'dict'>":
            classType = composeClassName(className, k) + "Model"
            header += "@property (nonatomic, strong) %s *%s;\n" % (classType, pname)
        elif ktype == "<type 'list'>":
            if len(v) > 0:
                it = v[0]
                t = str(type(it))
                nn = simpleTypeName(t)
                if nn == None :
                    varlist[pname] = composeClassName(className, k) + "Model"
                    header += "@property (nonatomic, strong) NSArray<%s> *%s;\n" % (varlist[pname], pname)
                    protocols.append(varlist[pname])
                else:
                    header += "@property (nonatomic, strong) NSArray *%s;\n" % (pname)
        else:
            header += "@property (nonatomic, strong) NSString *%s;\n" % pname
    protocol_string = ''
    for value in protocols:
        protocol_string += "@protocol %s\n@end\n" % (value)
    header += "@end"+"\n"
    print_color_string(protocol_string + header, "lred")
    classList[className] = varlist

def print_implemention(className , mapKeys):
    implementation = ("@implementation %s" % (className)) + "Model\n"

    if className ==  mainClass:
        implementation += '''
        - (NSString *)protocolUrl {
            return requestUrl(@"<#host#>", @"<#ver#>", @"<#path#>");
        }

        - (HYBHttp)method {
            return HYBHttp<#method#>;
        }

        - (NSString *)description {
            return @"<#接口描述#>";
        }
        '''    
    implementation += "@end"+"\n"
    print_color_string(implementation, "brown")

def make_json(s,className):
    global mainClass
    mainClass = className
    iterItem(s,className)
    print "\n\n\n\n"
    print "//for implementation"
    for k , v in classList.items():
        print_implemention(k,v)


