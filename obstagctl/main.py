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
# init argparse
def create_parser():
	parser = argparse.ArgumentParser(description='Программа для управления тегами в MarkDown-заметках')

	parser.add_argument(
		'-f',
		'--file',
		dest = 'file',
		type = str,
		help = 'Указать файл для обработки'
	)

	parser.add_argument(
		'-d',
		'--directory',
		dest = 'dir',
		type = str,
		help = 'Указать директорию, все файлы в которой будут обработаны ' +
			   '(укажите -r, чтобы обработать директорию рекурсивно)'
	)

	parser.add_argument(
		'-r',
		'--recursive',
		dest   = 'recursive',
		action = 'store_true',
		help   = 'Обработать указанную папку рекурсивно'
	)

	parser.add_argument(
		'-c',
		'--count',
		dest   = 'count',
		action = 'store_true',
		help   = 'Посчитать количество тегов и выдать в формате json'
	)

	parser.add_argument(
		'-m',
		'--map',
		dest = 'map',
		type = str,
		help = 'Заменить теги на другие; аргумент должен представлять из себя ' +
		'словарь в формате json. Пример: \'{ "определения" : "определения", "раз" : "два" }\''
	)

	parser.add_argument(
		'-M',
		'--no-md-only',
		dest   = 'nomdonly',
		action = 'store_true',
		help   = 'Обрабатывать все файлы, а не только с расширением md'
	)

	return parser





############################################################
# main
parser = create_parser()
args = parser.parse_args()

files = []

if args.file is not None:
	files.append(args.file)

if args.dir is not None:
	if args.recursive:
		recursive(
			args.dir,
			lambda f: files.append(f),
			onlyfiles=True
		)

	else:
		for fname in os.listdir(args.dir):
			files.append(fname)

if not args.nomdonly:
	files = list(filter(lambda f: len(f) > 2 and f[-2:] == 'md', files))

print(files)






# END
