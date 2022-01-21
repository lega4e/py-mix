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

	parser.add_argument(
		'files', nargs='*', default=None,
		help='Указать файлы для обработки; если аргументы отсутствуют, то ' +
		     'будут взяты все файлы с расширением mp3 из текущей либо ' +
         'указанной ключом -D директории'
	)

	parser.add_argument(
		'-D', '--dir', dest='dir', default='.', type=str,
		help='Указать, из какой папки брать файлы, если они не указаны явно'
	)

	parser.add_argument(
		'-n', '--name', dest='name', default=None, type=str,
		help='Установить название',
	)

	parser.add_argument(
		'-N', '--number', dest='number', default=None, type=int,
		help='Установить номер трека'
	)

	parser.add_argument(
		'-C', '--numerate-tracks', dest='numerate', default=False,
		action='store_true',
		help='Установить номер трека в соответствии с порядком аргумента ' +
		     'в командной строке / в папке'
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
		action='store_false',
		help='При получении полей из имени файла устанавливать не только ' +
		     'исполнителя, но и исполнителя альбома'
	)

	parser.add_argument(
		'-v', '--verbose', dest='verbose', default=False,
		action='store_true',
		help='Выводить каждую исполняемую команду'
	)

	parser.add_argument(
		'-f', '--fake', dest='fake', default=False,
		action='store_true',
		help='Не выполнять реальные команды (полезно с опцией -v)'
	)

	return parser





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             CONFIG                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def number2str(number, total):
	return ('%s%s' % (
		str(number or ''),
		'/' + str(total) if total else ''
	) or None)

def make_config(args):
	cfg        = args
	cfg.nameex = re.compile(r'^(?:(\d+)\.)?\s*(.*)\s* - \s*(.*)\.mp3$')
	cfg.setcom = 'id3v2 -2 --%s "%s" "%s"'
	cfg.remcom = 'id3v2 -r "%s" "%s"'
	cfg.files  = ( args.files if len(args.files) != 0 else
		[ f for f in os.listdir(cfg.dir) if re.match(r'.*\.mp3', f) ] )
	cfg.fields = list(filter(lambda x: x[1] is not None, [
		( TIT2, args.name                           ),
		( TRCK, number2str(args.number, args.total) ),
		( TPE1, args.artist                         ),
		( TPE2, args.albumartist                    ),
		( TALB, args.album                          ),
		( TCON, args.genre                          ),
		( PCNT, args.playcount                      ),
		( TYER, args.year                           ),
	]))

	return args





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                      ACCESSORY FUNCTIONS                       ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def set_field(cfg, frame, value, file):
	if value is None:
		return 0

	ret = 0

	if frame == TRCK:
		m = re.match(r'(\d+)?(?:/(\d+))?', value)
		n = int(m.group(1)) if m and m.group(1) else None
		t = int(m.group(2)) if m and m.group(2) else None

		if cfg.num is None and cfg.tot is None:
			cfg.num = n
			cfg.tot = t
		elif (
				(cfg.num is not None and cfg.tot is not None) or
				(cfg.num is     None and n       is     None) or
				(cfg.tot is     None and t       is     None)
		):
			return 0
		elif cfg.num is None:
			cfg.num = n
			t = cfg.tot
		else:
			cfg.tot = t
			n = cfg.num

		com   = cfg.remcom % (frame, file)
		cfg.verbose and print(com)
		ret   = -1 if not cfg.fake and os.system(com) != 0 else 0
		value = number2str(n, t)

	com = cfg.setcom % (frame, value, file)
	cfg.verbose and print(com)
	return -1 if not cfg.fake and os.system(com) != 0 else 0



def set_fields_by_filename(cfg, file):
	m = re.match(cfg.nameex, file)
	if m is None:
		print("Error: invalid name of file %s" % file, file=sys.stderr)
		return 1

	fields = [
			(cfg.number, TRCK, m.group(1)),
			(cfg.artist, TPE1, m.group(2)),
			(cfg.name,   TIT2, m.group(3)),
			*(cfg.sameartist and [ (cfg.albumartist, TPE2, m.group(2)) ] or [])
	]

	ret = 0
	for check, frame, value in fields:
		if check is not None or value is None:
			continue
		ret |= set_field(cfg, frame, value, file)

	return ret



def set_fields(cfg, file):
	ret = 0
	for frame, value in cfg.fields:
		ret |= set_field(cfg, frame, value, file)
	return ret



def add_genres(cfg, file):
	genres  = subprocess.check_output([ 'id3v2', '-R', '%s' % file ])
	genres  = genres.decode().split('\n')
	genres  = list(filter(lambda x: x.startswith(TCON), genres))
	if len(genres):
		genres = re.match(r'([^(]*)(\(\d+\))?', genres[0][6:]).group(1).strip()
	else:
		genres = ''
	genres  = map(lambda x: x.strip(), re.split(r'[^\w\s]', genres))
	genres  = list(filter(lambda x: x, genres))
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

	for i in range(len(cfg.files)):
		file = cfg.files[i]
		cfg.num = None
		cfg.tot = None

		cfg.verbose and print('File \'%s\'' % file)

		ret |= set_fields(cfg, file)
		if cfg.addgenres is not None:
			ret   |= add_genres(cfg, file)
		if cfg.numerate:
			total  = cfg.totalauto and len(cfg.files) or None
			ret   |= set_field(cfg, TRCK, number2str(i+1, total), file)
		elif cfg.totalauto:
			print(number2str(None, len(cfg.files)))
			ret   |= set_field(cfg, TRCK, number2str(None, len(cfg.files)), file)
		if cfg.parsefilename:
			ret   |= set_fields_by_filename(cfg, file)

		cfg.verbose and print()

	return ret


if __name__ == '__main__':
	exit(main())





# END
