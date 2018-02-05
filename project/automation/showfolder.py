
# defaults write com.apple.finder AppleShowAllFiles TRUE&&killall Finder
# defaults write com.apple.finder AppleShowAllFiles False&&killall Finder
import os
from util import *

def genDir(dir_path):
	os.system('chflags nohidden '+ dir_path);

map(genDir,set(readlines_from_stdin()))
