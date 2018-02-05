#coding=utf-8
import os,sys,string
from util import *
from mvc import mTempleh,mTemplem,vTempleh,vTemplem,cTempleh,cTemplem

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


lines = set(readlines_from_stdin())
map(genDir,lines)