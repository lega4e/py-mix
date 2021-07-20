#!/usr/bin/python3

import argparse
import os
import re
import sys





# objects
tag_re    = re.compile(r'#[\w_]+')
code_re   = re.compile(r'```')
incode_re = re.compile(r'`')





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



def tag_iter(data):
	inters = [ edge.span()[0] for edge in re.finditer(code_re, data) ]
	if len(inters) % 2 == 1:
		inters.append(len(data))
	inters = [ (inters[i], inters[i+1]) for i in range(0, len(inters), 2) ]

	inline = [ edge.span()[0] for edge in re.finditer(incode_re, data) ]
	inline = list(filter(lambda x: not contains(inters, x), inline))
	if len(inline) % 2 == 1:
		inline.append(len(data))
	inline = [ (inline[i], inline[i+1]) for i in range(0, len(inline), 2) ]

	inters.extend(inline)

	for tag in re.finditer(tag_re, data):
		if contains(inters, tag.span()[0]) or contains(inters, tag.span()[1]):
			continue

		yield tag

def replace_tags_data(data, repmap):
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
		help   = 'Обработать указанную (-d) папку рекурсивно'
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
# argument handling
def get_files(args):
	files = []

	# args
	if args.file is not None:
		if not os.path.isfile(args.file):
			print('Ошибка: файл "%s" не существует' % args.file, file=sys.stderr)
			exit(-1)
		files.append(args.file)

	if args.dir is not None:
		if args.recursive:
			recursive(
				args.dir,
				lambda f: files.append(f),
				onlyfiles=True )
		else:
			for fname in os.listdir(args.dir):
				files.append(fname)

	if not args.nomdonly:
		files = list(filter(lambda f: len(f) > 2 and f[-2:] == 'md', files))

	return files


def read_tagmap(map):
	try:
		tagmap = eval(map)
	except Exception as e:
		print('xError: ' + str(e), file=sys.stderr)
		exit(-1)

	tmp = {}
	for key, value in tagmap.items():
		if not isinstance(key, str) or not isinstance(value, str):
			print("Ошибка: элементы отображения должны быть строками", file=sys.stderr)
			exit(-1)

		if len(key) > 0 and key[0] != '#':
			key = '#' + key
		if len(value) > 0 and value[0] != '#':
			value = '#' + value

		tmp[key] = value

	return tmp





############################################################
# main actions
def count_tags(files):
	tags = {}

	for file in files:
		data = open(file).read()
		for match in tag_iter(data):
			tags[match.group()] = tags.get(match.group(), 0) + 1

	return tags


def replace_tags(files, tagmap):
	for file in files:
		data = replace_tags_data(open(file, 'r').read(), tagmap)
		open(file, 'w').write(data)





############################################################
# main
parser = create_parser()
args   = parser.parse_args()
files  = get_files(args)

if args.count:
	print(re.sub(r"'", r'"', str(count_tags(files))))
elif args.map:
	tagmap = read_tagmap(args.map)
	replace_tags(files, tagmap)
else:
	parser.print_help()
	exit(0)




# END
