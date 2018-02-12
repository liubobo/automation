from util import *
regex = r"\b[\w]*?(?=[;\n])"
matches = re.finditer(regex, ''.join([x+';' for x in readlines_from_stdin()]))

def printResult(result):
	try:
		print render_template(getControlType(result) + '.html', {'name': result})
	except:
		print render_template('costom' + '.html', {'name': result})


map(printResult,filter(lambda x:len(x),[str(match.group()).strip('\n').strip(' ') for match in matches]))



