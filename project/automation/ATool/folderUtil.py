import os
#coding=utf8
from Util import *
import objc

def mkdirs(dir_path):
	os.system('mkdir ~/Desktop/'+ dir_path);
















#useless
def hidden_folder(dir_path):
	os.system('chflags hidden '+ dir_path);

def show_folder(dir_path):
	os.system('chflags nohidden '+ dir_path)

def showAll():
    os.system('defaults write com.apple.finder AppleShowAllFiles TRUE&&killall Finder')

def hiddenAll():
    os.system('defaults write com.apple.finder AppleShowAllFiles False&&killall Finder')