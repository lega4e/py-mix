#!/usr/bin/python3

import argparse
import sys





# functions
tabsize = 4

def spaces2tabs(line):
	while True:
		pos = line.find(' '*tabsize)
		if pos < 0 or (line[:pos] != '' and not line[:pos].isspace()):
			break
		line = line[:pos] + '\t' + line[pos+tabsize:]
	return line

def tabs2spaces(line):
	count = 0
	for ch in line:
		if ch == '\t':
			count += 1
		else:
			break
	return ' ' * tabsize * count + line[count:]





# parser
parser = argparse.ArgumentParser(
	description="Replace space on line start with tabs or vice versa"
)

parser.add_argument(
	'-t', '--tabsize', dest='tabsize',
	help='Space per tab',
	type=int, default=tabsize
)

parser.add_argument(
	'-a', '--action', dest='action',
	help='s2t (spaces to tabs) or t2s (tab to spaces)',
	required=True, choices=['s2t', 't2s']
)

args = parser.parse_args()



# main
tabsize = args.tabsize
action  = args.action

try:
	while True:
		line = input()
		if action == 's2t':
			line = spaces2tabs(line)
		elif action == 't2s':
			line = tabs2spaces(line)
		print(line)
except EOFError:
	pass





# END
