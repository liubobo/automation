# from ios_code_generator import getter
from util import *

for x in readlines_from_stdin():
	result = str(x).strip('\n').strip(' ')
	if len(result) != 0:
		regex = r"[A-Z][a-z].*"
		matches = re.finditer(regex, result)
		for matchNum, match in enumerate(matches):	
			print '@property(nonatomic, strong)' + 'UI'+str(match.group())+'*'+str(x)+';'


