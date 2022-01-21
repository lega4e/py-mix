#!/usr/bin/python3

#
# Описание работы
#
# Для каждого mp3 файла программа парсит его имя, извлекая
# 1) номер дорожки,
# 2) исполнителя,
# 3) название.
# Номер дорожки опционален. Файлы должны быть названы по следующему
# шаблону: <номер>.<Исполнитель> - <Название>.mp3. Подробнее см.
# переменную nameex.
#
# Спарисв файлы, программа устанавливает соответствующие
# теги с помощью утилиты id3v2
#

import argparse as ap
import os
import re
import subprocess
import sys





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                           CONSTANTS                            ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

TIT2 = 'TIT2' # Название
TRCK = 'TRCK' # Номер трека и общее количество
TPE1 = 'TPE1' # Исполнитель
TPE2 = 'TPE2' # Исполнитель альбома
TALB = 'TALB' # Альбом
TCON = 'TCON' # Жанр
PCNT = 'PCNT' # Количество прослушиваний
TYER = 'TYER' # Год





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                        ARGUMENT PARSER                         ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def make_parser():
	parser = ap.ArgumentParser(description='Программа для установки тегов IDv2')

	parser.add_argument('files', nargs='*')

	parser.add_argument(
		'-n', '--name', dest='name', default=None, type=str,
		help='Установить название',
	)

	parser.add_argument(
		'-N', '--number', dest='number', default=None, type=int,
		help='Установить номер трека'
	)

	parser.add_argument(
		'-t', '--total-tracks', dest='total', default=None, type=int,
		help='Установить количество треков в альбоме'
	)

	parser.add_argument(
		'-T', '--total-tracks-auto', dest='totalauto', default=False,
		action='store_true',
		help='Установить количество треков в альбоме по количеству ' +
		     'обрабатываемых файлов'
	)

	parser.add_argument(
		'-a', '--artist', dest='artist', default=None, type=str,
		help='Установить исполнителя',
	)

	parser.add_argument(
		'-A', '--albumartist', dest='albumartist', default=None, type=str,
		help='Установить исполнителя альбома',
	)

	parser.add_argument(
		'-l', '--album', dest='album', default=None, type=str,
		help='Установить альбом',
	)

	parser.add_argument(
		'-c', '--play-count', dest='playcount', default=None, type=int,
		help='Установить количество прослушиваний',
	)

	parser.add_argument(
		'-g', '--genre', dest='genre', default=None, type=str,
		help='Установить жанр',
	)

	parser.add_argument(
		'-G', '--add-genres', dest='addgenres', default=None, type=str,
		help='Добавить жанры к существующим; если жанров несколько ' +
		     'они должны быть разделены любыми символами [^\w\s]',
	)

	parser.add_argument(
		'-s', '--sort-genres', dest='sortgenres', default=False,
		action='store_true',
		help='Отсортировать жанры'
	)

	parser.add_argument(
		'-d', '--genre-delimiter', dest='genredelimeter', default=';', type=str,
		help='Символ, которым будут разделены жанры; не может быть буквой, ' +
		     'цифрой или пробельным символом'
	)

	parser.add_argument(
		'-y', '--year', dest='year', default=None, type=int,
		help='Установить год'
	)

	parser.add_argument(
		'-p', '--parse-filename', dest='parsefilename', default=False,
		action='store_true',
		help='Извлекает из названия файла номер трека (опционально) ' +
		     'исполнителя и название (подробнее см. регулярку в исходниках); ' +
				 'если установлены другие флаги, записывающие те же поля, то ' +
				 'будут использованы они'
	)

	parser.add_argument(
		'-L', '--same-artist', dest='sameartist', default=True,
		action='store_true',
		help='При получении полей из имени файла устанавливать не только ' +
		     'исполнителя, но и исполнителя альбома'
	)

	parser.add_argument(
		'-v', '--verbose', dest='verbose', default=False,
		action='store_true',
		help='Выводить каждую исполняемую команду'
	)

	return parser





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             CONFIG                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def make_config(args: ap.Namespace):
	cfg        = args
	cfg.nameex = re.compile(r'^(?:(\d+)\.)?\s*(.*)\s* - \s*(.*)\.mp3$')
	cfg.setcom = 'id3v2 -2 --%s "%s" "%s"'
	cfg.getcom = 'id3v2 -R "%s" | grep "%s" | cut -d' ' -f2- | sed -e "s/\s\+([0-9]\+)$//"'
	cfg.files  = ( args.files if len(args.files) != 0 else
		[ f for f in os.listdir() if re.match(r'.*\.mp3', f) ] )
	cfg.fields = list(filter(lambda x: x[1] is not None, [
		( TIT2, args.name        ),
		( TRCK, '%s%s' % (
			str(args.num or ''),
			'/' + str(args.total)
				if args.total else ''
		) or None                  ),
		( TPE1, args.artist      ),
		( TPE2, args.albumartist ),
		( TALB, args.album       ),
		( TCON, args.genre       ),
		( PCNT, args.playcount   ),
		( TYER, args.year        ),
	]))

	return args





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                      ACCESSORY FUNCTIONS                       ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def set_field(cfg, frame, value, file):
	com = cfg.com % (frame, value, file)
	cfg.verbose and print(com)
	return -1 if os.system(com) != 0 else 0



def set_fields_by_filename(cfg, file):
	m = re.match(cfg.tmpl, file)
	if m is None:
		print("Error: invalid name of file %s" % file, file=sys.stderr)
		return 1

	fields = [
			(cfg.number, TRCK, m.group(1)),
			(cfg.artist, TPE1, m.group(2)),
			(cfg.name,   TIT2, m.group(3)),
			*(cfg.sameartist and [ cfg.albumartist, TPE2, m.group(2) ] or [])
	]

	ret = 0
	for check, frame, value in fields:
		if check is not None:
			continue
		ret |= set_field(cfg, frame, value, file)

	return ret



def set_fields(cfg, file):
	ret = 0
	for frame, value in cfg.field:
		ret |= set_field(cfg, frame, value, file)
	return ret



def add_genres(cfg, file):
	genres  = subprocess.check_output(cfg.getcom % (file, TCON))
	genres  = list(map(lambda x: x.strip(), re.split(r'[^\w\s]', genres)))
	genres += list(map(lambda x: x.strip(), re.split(r'[^\w\s]', cfg.addgenres)))
	cfg.sortgenres and genres.sort()
	genres  = cfg.genredelimeter.join(genres)
	return set_field(cfg, TCON, genres, file)





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                              MAIN                              ~~~~~ #
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
