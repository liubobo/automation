from util import *

regex = r"\b[\w]*?(?=[;\n])"
matches = re.finditer(regex, ''.join([x+';' for x in readlines_from_stdin()]))

def printResult(result):
	print render_template(getControlType(result) + '.html', {'name': result})

map(printResult,filter(lambda x:len(x),[str(match.group()).strip('\n').strip(' ') for match in matches]))



