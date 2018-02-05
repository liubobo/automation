import os
from util import *

def genDir(dir_path):
	os.system('mkdir ~/Desktop/'+ dir_path);

map(genDir,set(readlines_from_stdin()))



