#!/usr/bin/python3

import sys





# functions
def spaces2tabs(line):
	while True:
		pos = line.find(' '*tabsize)
		if pos < 0 or (line[:pos] != '' and not line[:pos].isspace()):
			break
		line = line[:pos] + '\t' + line[pos+4:]
	return line

def tabs2spaces(line):
	count = 0
	for ch in line:
		if ch == '\t':
			count += 1
		else:
			break
	return ' ' * tabsize * count + line[count:]





# main
tabsize = 4

mode = None if len(sys.argv) == 1 else sys.argv[1]

try:
	while True:
		line = input()
		if mode == 's2t':
			line = spaces2tabs(line)
		elif mode == 't2s':
			line = tabs2spaces(line)
		print(line)
except EOFError:
	pass





# END
