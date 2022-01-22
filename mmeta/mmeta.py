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
import mutagen
import os
import re
import subprocess as sbprc
import sys

from mutagen import id3, flac





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                 CONSTANTS AND GLOBAL VARIABLES                 ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# flac
NAME      = 'title'
ARTIST    = 'artist'
ALBARTIST = 'albumartist'
ALBUM     = 'album'
TRACKNUM  = 'tracknumber'
TRACKTOT  = 'tracktotal'
TRACK     = 'track'
GENRE     = 'genre'
YEAR      = 'date'
COMMENT   = 'description'
CD        = None
PLAYCNT   = None

# ID3
TIT2 = 'TIT2' # Название
TRCK = 'TRCK' # Номер трека и общее количество
TPE1 = 'TPE1' # Исполнитель
TPE2 = 'TPE2' # Исполнитель альбома
TALB = 'TALB' # Альбом
TCON = 'TCON' # Жанр
PCNT = 'PCNT' # Количество прослушиваний
TYER = 'TYER' # Год
TPOS = 'TPOS' # Номер дииска (CD)
COMM = 'COMM' # Комментарий

# global variables
cfg = None





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
		'-d', '--dir', dest='dir', default='.', type=str,
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
		'-c', '--play-count', dest='playcnt', default=None, type=int,
		help='Установить количество прослушиваний',
	)

	parser.add_argument(
		'-g', '--genre', dest='genre', default=None, type=str,
		help='Установить жанр',
	)

	parser.add_argument(
		'-G', '--add-genre', dest='addgenres', default=None, type=str,
		help='Добавить жанры к существующим; если жанров несколько ' +
		     'они должны быть разделены любыми символами [^\w\s]',
	)

	parser.add_argument(
		'-s', '--sort-genre', dest='sortgenres', default=False,
		action='store_true',
		help='Отсортировать жанры'
	)

	parser.add_argument(
		'-D', '--genre-delimiter', dest='gendel', default=';', type=str,
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
		'-S', '--same-artist', dest='sameartist', default=True,
		action='store_false',
		help='При получении полей из имени файла устанавливать не только ' +
		     'исполнителя, но и исполнителя альбома (по умолчанию включено; ' +
				 'используйте этот флаг, чтобы отключить)'
	)

	parser.add_argument(
		'-L', '--same-album', dest='samealbum', default=False,
		action='store_true',
		help='При получении полей из имени файла устанавливать альбом ' +
		     'в исполнителя'
	)

	parser.add_argument(
		'-b', '--artist-as-directory', dest='artdir', default=False,
		action='store_true',
		help='Установить исполнителя в название директории файла'
	)

	parser.add_argument(
		'-B', '--album-artist-as-direcotry', dest='albartdir', default=False,
		action='store_true',
		help='Установить исполнителя альбома в название директории файла'
	)


	parser.add_argument(
		'-e', '--album-direcotry', dest='albdir', default=False,
		action='store_true',
		help='Установить альбом в название директории файла'
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
# ~~~~~                              META                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Track:
	def __init__(self, number, total):
		self.n = number;
		self.t = total

	def __eq__(self, other):
		return self.n == other.n and self.t == other.t


class Genre:
	def __init__(self, genre):
		self.g = genre

	def __str__(self):
		return genre2str(self.g)

	def __eq__(self, other):
		return self.g == other.g

	@staticmethod
	def from_str(genre):
		return Genre(str2genre(genres))


class Meta:
	def __init__(
		self,
		name:      str   = None,
		artist:    str   = None,
		albartist: str   = None,
		album:     str   = None,
		track:     Track = None
		genre:     Genre = None,
		playcnt:   int   = None,
		year:      int   = None,
		cd:        int   = None,
		comment:   str   = None,
	):
		self.name      = name
		self.artist    = artist
		self.albartist = albartist
		self.album     = album
		self.track     = track
		self.genre     = genre
		self.playcnt   = playcnt
		self.year      = year
		self.cd        = cd
		self.comment   = comment





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             QUERY                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Query:
	def __init__(
		self,
		new: Meta             = None,
		old: Meta             = None,
		mut: mutagen.FileType = None,
	):
		self.new = new
		self.old = old
		self.mut = mut






# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                           ACCESSORY                            ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def extension(file: str, error_if_no=True):
	l = list(filter(lambda x: x, file.split('.')))
	if len(l) < 2:
		if error_if_no:
			raise ValueError('File has no extension: %s' % file)
		return None
	return l[-1]



def track2str(number: int, total: int) -> str:
	return ('%s%s' % (
		str(number)      if number is not None else '',
		'/' + str(total) if total  is not None else ''
	))

def str2track(track: str) -> (int, int):
	if track is None:
		return (None, None)
	m = re.match(r'(\d+)?(?:/(\d+))?', track)
	try:
		number = int(m.group(1))
		total  = int(m.group(2))
	except:
		raise ValueError(track)
	return (number, total)


def genre2str(genres: [ str ]) -> str:
	if genre is None:
		return None
	return cfg.gendel.join(genre)

def str2genre(genres: str) -> [ str ]:
	if genre is None:
		return None
	return list(filter(
		lambda x: x,
		map(lambda x: x.strip(), re.split('[%s]' % cfg.agendels, genre)
	))





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                       FUNCTIONS FOR META                       ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def meta_from_mp3(file):
	try:    tags = id3.ID3(file)
	except: raise ValueError(file)

	int_or_none = lambda x: None if x is None else int(x)
	extract     = lambda x: None if x is None else str(x)

	return Meta(
		name      = extract(tags.get(TIT2)),
		artist    = extract(tags.get(TPE1)),
		albartist = extract(tags.get(TPE2)),
		album     = extract(tags.get(TALB)),
		tracknum  = str2track(extract(tags.get(TRCK)))[0],
		tracktot  = str2track(extract(tags.get(TRCK)))[1],
		genre     = str2genre(extract(tags.get(TCON))),
		playcnt   = int_or_none(extract(tags.get(PCNT))),
		year      = int_or_none(extract(tags.get(TYER))),
		cd        = int_or_none(extract(tags.get(TPOS))),
		comment   = extract(tags.get(COMM)),
	)



def meta_from_flac(file):
	try:    tags = flac.FLAC(file)
	except: raise ValueError(file)

	int_or_none = lambda x: None if x is None else int(x)
	extract     = lambda x: None if x is None else x[0]
	extractg    = lambda x: None if x is None else cfg.agendels[0].join(x)

	return Meta(
		name      = extract(tags.get(NAME)),
		artist    = extract(tags.get(ARTIST)),
		albartist = extract(tags.get(ALBARTIST)),
		album     = extract(tags.get(ALBUM)),
		tracknum  = int_or_none(extract(tags.get(TRACKNUM))),
		tracktot  = int_or_none(extract(tags.get(TRACKTOT))),
		genre     = str2genre(extractg(tags.get(GENRE))),
		playcnt   = None,
		year      = int_or_none(extract(tags.get(YEAR))),
		cd        = None,
		comment   = extract(tags.get(COMMENT)),
	)



def meta_from_file(file):
	ex = extension(file)

	if ex == 'mp3':
		return meta_from_mp3(file)
	elif ex == 'flac':
		return meta_from_flac(file)
	else:
		raise ValueError('Unknown format: %s' % l[-1])





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                        QUERY FUNCTIONS                         ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class QueryUnit:
	def __init__(self, id3, flac, old, new):
		self.id3  = id3
		self.flac = flac
		self.old  = old
		self.new  = new



def set_tag(u: QueryUnit, mut):
	if u.new == u.old:
		return

	if isinstance(mut, id3.ID3):
		if u.id3 is not None:
			mut.setall(u.id3, [ eval('id3.%s(3, "%s")' % (u.id3, str(u.new))) ])
	elif isinstance(mut, flac.FLAC):
		if u.flac == TRACK:
			mut[TRACKNUM] = u.new.n
			mut[TRACKTOT] = u.new.t
		elif u.flac is not None:
			mut[u.flac] = u.new
	else:
		raise TypeError('Unknown type: %s' % type(mut))



def process_query(q: Query, file: str):
	tags = [
			QueryUnit(TIT2, NAME,      q.old.name,      q.new.name),
			QueryUnit(TPE1, ARTIST,    q.old.artist,    q.new.artist),
			QueryUnit(TPE2, ALBARTIST, q.old.albartist, q.new.albartist),
			QueryUnit(TALB, ALBUM,     q.old.album,     q.new.album),
			QueryUnit(TCON, GENRE,     q.old.genre,     q.new.genre),
			QueryUnit(TRCK, TRACK,     q.old.track,     q.old.track),
			QueryUnit(TYER, YEAR,      q.old.year,      q.new.year),
			QueryUnit(TPOS, CD,        q.old.cd,        q.new.cd),
			QueryUnit(PCNT, PLAYCNT,   q.old.playcnt,   q.new.playcnt),
			QueryUnit(COMM, COMMENT,   q.old.comment,   q.new.comment),
	]

	if q.mut is None:
		q.mut = mutagen.FileType(file)

	for tag in tags:
		set_tag(tag, q.mut)





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             CONFIG                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #



def make_config(args):
	global cfg
	cfg          = args
	cfg.agendels = '/;|'
	cfg.nameex   = re.compile(r'^(?:(\d+)\.)?\s*(.*)\s* - \s*(.*)\.mp3$')
	cfg.setcom   = 'id3v2 -2 --%s "%s" "%s"'
	cfg.remcom   = 'id3v2 -r "%s" "%s"'
	cfg.files    = ( args.files if len(args.files) != 0 else
		[ f for f in os.listdir(cfg.dir) if re.match(r'.*\.mp3', f) ] )
	cfg.fields = list(filter(lambda x: x[1] is not None, [
		( TIT2, args.name                                  ),
		( TRCK, track2str(args.number, args.total) or None ),
		( TPE1, args.artist                                ),
		( TPE2, args.albumartist                           ),
		( TALB, args.album                                 ),
		( TCON, args.genre                                 ),
		( PCNT, args.playcnt                               ),
		( TYER, args.year                                  ),
	]))

	return args





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                         CORE FUNCTIONS                         ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def remove_duplicates(l: list):
	res = []
	for val in l:
		if val not in res:
			res.append(val)
	return res



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
	m = re.match(cfg.nameex, os.path.basename(file))
	if m is None:
		print("Error: invalid name of file %s" % file, file=sys.stderr)
		return 1

	fields = [
			(cfg.number, TRCK, m.group(1)),
			(cfg.artist, TPE1, m.group(2)),
			(cfg.name,   TIT2, m.group(3)),
			*(cfg.sameartist and [ (cfg.albumartist, TPE2, m.group(2)) ] or []),
			*(cfg.samealbum  and [ (cfg.album,       TALB, m.group(2)) ] or []),
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



def add_genre(cfg, file):
	genre  = sbprc.check_output([ 'id3v2', '-R', '%s' % file ])
	genre  = genres.decode().split('\n')
	genre  = list(filter(lambda x: x.startswith(TCON), genres))
	if len(genre):
		genre = re.match(r'([^(]*)(\(\d+\))?', genres[0][6:]).group(1).strip()
	else:
		genre = ''
	genre  = list(map(lambda x: x.strip(), re.split(r'[^\w\s]', genres)))
	genre += list(map(lambda x: x.strip(), re.split(r'[^\w\s]', cfg.addgenres)))
	genre  = list(filter(lambda x: x, genres))
	cfg.sortgenre and genres.sort()
	genre  = remove_duplicates(genres)
	genre  = cfg.gendel.join(genres)
	return set_field(cfg, TCON, genre, file)





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                              MAIN                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def main():
	cfg = make_config(make_parser().parse_args())
	ret = 0

	cfg.verbose and print()

	for i in range(len(cfg.files)):
		file = cfg.files[i]
		cfg.num = None
		cfg.tot = None

		cfg.verbose and print('File \'%s\'' % file)

		ret |= set_fields(cfg, file)
		if cfg.addgenre is not None:
			ret   |= add_genre(cfg, file)
		if cfg.numerate:
			total  = cfg.totalauto and len(cfg.files) or None
			ret   |= set_field(cfg, TRCK, number2str(i+1, total), file)
		elif cfg.totalauto:
			ret   |= set_field(cfg, TRCK, number2str(None, len(cfg.files)), file)
		if cfg.parsefilename:
			ret   |= set_fields_by_filename(cfg, file)

		cfg.verbose and print()

	return ret


if __name__ == '__main__':
	exit(main())





# END
