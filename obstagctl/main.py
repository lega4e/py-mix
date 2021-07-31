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





############################################################
# main
def main():
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



if __name__ == '__main__':
	main()





# END
