#!/usr/bin/python3

import argparse
import os
import re





# help functions
def recursive(root, fun, onlyfiles=False):
	for file in os.listdir(root):
		file = os.path.join(root, file)
		if not onlyfiles or os.path.isfile(file):
			fun(file)
		if os.path.isdir(file):
			recursive(file, fun)
	return

def contains(inters, val):
	for inter in inters:
		if inter[0] <= val <= inter[1]:
			return True
	return False





# objects
tag_re  = re.compile(r'#[\w_]+')
code_re = re.compile(r'```')
dname   = '/home/lis/.local/obsidian/main/Zettelkasten'





# core functions
def tag_iter(data):
	inters = [ edge.span()[0] for edge in re.finditer(code_re, data) ]
	if len(inters) % 2 == 1:
		inters.append(len(data))
	inters = [ (inters[i], inters[i+1]) for i in range(0, len(inters), 2) ]

	for tag in re.finditer(tag_re, data):
		if contains(inters, tag.span()[0]) or contains(inters, tag.span()[1]):
			continue

		yield tag


def count_tags(dname):
	tags = {}

	for fname in sorted(os.listdir(dname)):
		if len(fname) < 2 or fname[-2:] != 'md':
			continue

		data = open(os.path.join(dname, fname)).read()
		for match in tag_iter(data):
			tags[match.group()] = tags.get(match.group(), 0) + 1


def replace_tags(data, repmap):
	pos = 0
	res = ''
	for tag in tag_iter(data):
		res += data[pos:tag.span()[0]]
		res += repmap.get(tag.group(0), tag.group(0))
		pos  = tag.span()[1]

	res += data[pos:]
	return res





############################################################
# main
replace_tags(open(dname + '/Смерть-советчик.md').read(), {'#эзотерика' : '#чушь'})





# END
