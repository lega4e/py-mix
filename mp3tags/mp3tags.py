#!/usr/bin/python3

#
# Описание работы
#
# Для каждого mp3 файла программа парсит его имя, извлекая 1) номер дорожки,
# 2) исполнителя, 3) название. Номер дорожки опционален. Файлы должны быть
# названы по следующему шаблону: <номер>.<Исполнитель> - <Название>.mp3.
# Подробнее см. переменную tmpl.
#
# Спарисв файлы, программа устанавливает соответствующие теги с помощью утилиты
# id3v2
#

import os
import re
import sys
import argparse as ap



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                        argument parser                         ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def make_parser():
	parser = ap.ArgumentParser(description='Программа для установки тегов IDv2')

	parser.add_argument('-a', '--album', dest='album', default='Избранное')
	parser.add_argument('-g', '--genre', dest='genre', default='')
	parser.add_argument('files', nargs='*')

	return parser



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             config                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Config:
	def __init__(self, tmpl, com, fields, files):
		self.tmpl   = tmpl
		self.com    = com
		self.fields = fields
		self.files  = files

def make_config(args: ap.Namespace):
	tmpl   = re.compile(r'^(?:(\d+)\.)?\s*(.*)\s* - \s*(.*)\.mp3$')
	com    = 'id3v2 -2 --%s "%s" "%s"'
	fields = [
		( 'TRCK', lambda m: m.group(1) ), # Номер трека
		( 'TPE1', lambda m: m.group(2) ), # Исполнитель
		( 'TPE2', lambda m: m.group(2) ), # Исполнитель альбома
		( 'TIT2', lambda m: m.group(3) ), # Название
		( 'TALB', lambda m: args.album ), # Альбом
		( 'TCON', lambda m: args.genre ), # Жанр
	]
	files  = ( args.files if len(args.files) != 0 else
		[ f for f in os.listdir() if re.match(r'.*\.mp3', f) ] )

	return Config(
		tmpl   = tmpl,
		com    = com,
		fields = fields,
		files  = files
	)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                              main                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def main():
	cfg = make_config(make_parser().parse_args())
	ret = 0

	for file in cfg.files:
		m = re.match(cfg.tmpl, file)

		if m is None:
			print("Error: invalid name of file %s" % file, file=sys.stderr)
			ret = 1
			continue

		for flag, getval in cfg.fields:
			com = cfg.com % (flag, getval(m) or '', file)
			print(com)
			os.system(com)

		print()

	return ret


if __name__ == '__main__':
	exit(main())



# END
