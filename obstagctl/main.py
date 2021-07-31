#!/usr/bin/python3

import argparse
import os
import re
import sys

from aux    import recursive
from parser import create_parser, get_files, read_tagmap
from core   import tag_iter, replace_tags_in_string





############################################################
# main actions
def count_tags(files: [ str ]) -> { str : int }:
	'''
	Считает количество использований каждого тега
	'''
	tags = {}

	for file in files:
		data = open(file).read()
		for match in tag_iter(data):
			tags[match.group()] = tags.get(match.group(), 0) + 1

	return tags


def replace_tags(files: [ str ], tagmap: { str : str }):
	'''
	Заменяет все теги в соответствии с отображением во
	всех переданных файлах.
	'''
	for fname in files:
		data = replace_tags_in_string(open(fname, 'r').read(), tagmap)
		open(fname, 'w').write(data)


def check_files(files, recursive):
	if len(files) == 0:
		if not recursive:
			print('Ошибка: Файлы не найдены; попробуйте ключ -r (--recursive)', file=sys.stderr)
		else:
			print('Ошибка: Файлы не найдены', file=sys.stderr)
		exit(-1)





############################################################
# main
def main():
	parser = create_parser()
	args   = parser.parse_args()

	try:
		files  = get_files(args)
	except Exception as e:
		print("Ошибка: " + str(e), file=sys.stderr)
		exit(-1)

	if args.count or args.count_total:
		check_files(files, args.recursive)
		tags = count_tags(files)

		if args.json_output:
			result = {}
		else:
			result = ''

		if args.count_total:
			if args.json_output:
				result['total'] = len(tags)
			else:
				result += 'Различных тегов: %i\n' % len(tags)

		if args.count:
			if args.json_output:
				result['tags'] = tags
			else:
				sorted_tags = [ (tag, count) for tag, count in tags.items() ]
				sorted_tags.sort(key=lambda x: x[1], reverse=True)
				for tag, count in sorted_tags:
					result += '%s: %i\n' % (tag, count)

		if args.json_output:
			print(re.sub(r"'", r'"', str(result)))
		else:
			print(result)
	elif args.map:
		try:
			tagmap = read_tagmap(args.map)
		except Exception as e:
			print("Ошибка: " + str(e), file=sys.stderr)
			exit(-1)
		check_files(files, args.recursive)
		replace_tags(files, tagmap)
	else:
		print('Укажите действие')
		exit(-1)



if __name__ == '__main__':
	main()





# END
