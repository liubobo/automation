import os 

def traverse(f,old,new):  
    fs = os.listdir(f)  
    for f1 in fs:  
		tmp_path = os.path.join(f,f1)
		if tmp_path.startswith('.'):
			continue
		if  os.path.isdir(tmp_path):
			traverse(tmp_path,old,new)
		else:
			if f1.startswith(old):
				os.rename(tmp_path,os.path.join(f,f1.replace(old,new)) )


