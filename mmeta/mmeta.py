#!/usr/bin/python3

#
# Алгоритм:
# 1. Считать аргументы командной строки, установить конфиг
# 2. Обработать все предоставленные файлы:
#    - Считать текущие значения
#    - Сформировать запрос изменения тегов в зависимости от аргументов
#    - Обработать запрос
#
# TODO: artist as dir
# TODO: albartist as dir
# TODO: album as dir
#

import argparse as ap
import mutagen
import re
import subprocess as sbprc

from copy    import deepcopy
from mutagen import id3, mp3, flac
from os      import listdir
from os.path import abspath, basename, join
from sys     import stderr





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                 CONSTANTS AND GLOBAL VARIABLES                 ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

ALLOWED_GENDELS = ';/|'

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
    '-N', '--number', dest='tracknum', default=None, type=int,
    help='Установить номер трека'
  )

  parser.add_argument(
    '-C', '--numerate-tracks', dest='numerate', default=False,
    action='store_true',
    help='Установить номер трека в соответствии с порядком аргумента ' +
         'в командной строке / в папке'
  )

  parser.add_argument(
    '-t', '--total-tracks', dest='tracktot', default=None, type=int,
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
    '-A', '--albumartist', dest='albartist', default=None, type=str,
    help='Установить исполнителя альбома',
  )

  parser.add_argument(
    '-l', '--album', dest='album', default=None, type=str,
    help='Установить альбом',
  )

  parser.add_argument(
    '-p', '--play-count', dest='playcnt', default=None, type=int,
    help='Установить количество прослушиваний',
  )

  parser.add_argument(
    '-g', '--genre', dest='genre', default=None, type=str,
    help='Установить жанр',
  )

  parser.add_argument(
    '-G', '--add-genres', dest='addgenres', default=None, type=str,
    help='Добавить жанры к существующим; если жанров несколько ' +
         'они должны быть разделены любыми символами %s' % ALLOWED_GENDELS,
  )

  parser.add_argument(
    '-s', '--sort-genres', dest='sortgenres', default=False,
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
    '-c', '--cd', dest='cd', default=None, type=int,
    help='Номер CD-диска',
  )

  parser.add_argument(
    '-M', '--comment', dest='comment', default=None, type=str,
    help='Установить комментарий'
  )

  parser.add_argument(
    '-F', '--parse-filename', dest='parsefilename', default=False,
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
    '-B', '--albumartist-as-direcotry', dest='albartdir', default=False,
    action='store_true',
    help='Установить исполнителя альбома в название директории файла'
  )

  parser.add_argument(
    '-e', '--album-as-direcotry', dest='albdir', default=False,
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
  def __init__(self, number: int, total: int):
    self.n = number;
    self.t = total

  def __str__(self):
    return track2str(self.n, self.t)

  def __eq__(self, other):
    return self.n == other.n and self.t == other.t


class Genre:
  def __init__(self, genre: [ str ]):
    self.g = genre

  def __str__(self):
    return genre2str(self.g)

  def __eq__(self, other):
    return self.g == other.g

  @staticmethod
  def from_str(genre):
    return Genre(str2genre(genres))


class Meta:
  'Represents meta information all of track the program work with'
  def __init__(
    self,
    name:      str   = None,
    artist:    str   = None,
    albartist: str   = None,
    album:     str   = None,
    track:     Track = None,
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
  'Represents query for changing one track'
  def __init__(
    self,
    new: Meta             = None,
    old: Meta             = None,
    mut: mutagen.FileType = None,
  ):
    self.new = new
    self.old = old
    self.mut = mut


class QueryUnit:
  'Represents query for changing a single tag in track'
  def __init__(self, id3: str, flac: str, old, new):
    self.id3  = id3
    self.flac = flac
    self.old  = old
    self.new  = new





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                      ACCESSORY FUNCTIONS                       ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def extension(file: str, error_if_no=True):
  l = list(filter(lambda x: x, file.split('.')))
  if len(l) < 2:
    if error_if_no:
      raise ValueError('File has no extension: %s' % file)
    return None
  return l[-1]

def remove_duplicates(l: list):
  res = []
  for val in l:
    if val not in res:
      res.append(val)
  return res

def confirm_interface(file: str, mut: mutagen.FileType=None):
  if mut is None:
    try:    mut = mutagen.File(file)
    except: raise ValueError('Can\'t open file "%s"' % file)
  return mut



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ converting ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Если передать None, вернёт None

def track2str(number: int, total: int) -> str:
  return ('%s%s' % (
    str(number)      if number is not None else '',
    '/' + str(total) if total  is not None else ''
  ))

def str2track(track: str) -> (int, int):
  if track is None:
    return (None, None)
  m = re.match(r'(-?\d+)?(?:/(-?\d+))?', track)
  try:    return int(m.group(1)), int(m.group(2))
  except: raise ValueError('Invalid track number or total track: "%s"' % track)


def genre2str(genre: [ str ]) -> str:
  if genre is None:
    return None
  return cfg.gendel.join(genre)

def str2genre(genre: str) -> [ str ]:
  if genre is None:
    return None
  return (list(filter(
    lambda x: x,
    map(lambda x: x.strip(), re.split('[%s]' % cfg.agendels, genre))
  )) or None)





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                       FUNCTIONS FOR META                       ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def meta_from_file(file: str, mut: mutagen.FileType):
  ex = extension(file)

  if ex == 'mp3':
    return meta_from_mp3(file, mut)
  elif ex == 'flac':
    return meta_from_flac(file, mut)
  else:
    raise TypeError()



def meta_from_mp3(file, mut: mp3.MP3):
  int_or_none = lambda x: None if x is None else int(x)
  extract     = lambda x: None if x is None else x.text[0]
  extracti    = lambda x: None if x is None else int(x.text[0])
  extractpcnt = lambda x: None if x is None else x.count
  extracttrk  = lambda x: None if x is None else Track(*str2track(x.text[0]))
  extractgnr  = lambda x: None if x is None else Genre(str2genre(x.text[0]))

  return Meta(
    name      = extract(mut.get(TIT2)),
    artist    = extract(mut.get(TPE1)),
    albartist = extract(mut.get(TPE2)),
    album     = extract(mut.get(TALB)),
    track     = extracttrk(mut.get(TRCK)),
    genre     = extractgnr(mut.get(TCON)),
    playcnt   = extractpcnt(mut.get(PCNT)),
    year      = extracti(mut.get(TYER)),
    cd        = extracti(mut.get(TPOS)),
    comment   = extract(mut.get(COMM)),
  )



def meta_from_flac(file, mut):
  int_or_none = lambda x: None if x is None else int(x[0])
  extract     = lambda x: None if x is None else x[0]
  extractg    = lambda x: (None if x is None else
                           Genre(str2genre(cfg.agendels[0].join(x))))
  extracttrk  = lambda x, y: (None if x is None and y is None else
                              Track(int_or_none(x), int_or_none(y)))

  return Meta(
    name      = extract(mut.get(NAME)),
    artist    = extract(mut.get(ARTIST)),
    albartist = extract(mut.get(ALBARTIST)),
    album     = extract(mut.get(ALBUM)),
    track     = extracttrk(mut.get(TRACKNUM), mut.get(TRACKTOT)),
    genre     = extractg(mut.get(GENRE)),
    playcnt   = None,
    year      = int_or_none(mut.get(YEAR)),
    cd        = None,
    comment   = extract(mut.get(COMMENT)),
  )





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                        QUERY FUNCTIONS                         ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def process_query(q: Query, file: str):
  tags = [
    QueryUnit(TIT2, NAME,      q.old.name,      q.new.name),
    QueryUnit(TPE1, ARTIST,    q.old.artist,    q.new.artist),
    QueryUnit(TPE2, ALBARTIST, q.old.albartist, q.new.albartist),
    QueryUnit(TALB, ALBUM,     q.old.album,     q.new.album),
    QueryUnit(TCON, GENRE,     q.old.genre,     q.new.genre),
    QueryUnit(TRCK, TRACK,     q.old.track,     q.new.track),
    QueryUnit(TYER, YEAR,      q.old.year,      q.new.year),
    QueryUnit(TPOS, CD,        q.old.cd,        q.new.cd),
    QueryUnit(PCNT, PLAYCNT,   q.old.playcnt,   q.new.playcnt),
    QueryUnit(COMM, COMMENT,   q.old.comment,   q.new.comment),
  ]

  q.mut = confirm_interface(file, q.mut)
  for tag in tags:
    set_tag(tag, q.mut)



def set_tag(u: QueryUnit, mut):
  if u.new == u.old:
    return

  if isinstance(mut, mp3.MP3):
    if u.id3 is not None:
      if u.id3 == PCNT:
        mut[u.id3] = eval('id3.%s(%s)' % (u.id3, str(u.new)))
      else:
        mut[u.id3] = eval('id3.%s(3, "%s")' % (u.id3, str(u.new)))
      cfg.verbose and print('%s = %s' % (u.id3, str(u.new)))
  elif isinstance(mut, flac.FLAC):
    if u.flac == TRACK:
      mut[TRACKNUM] = str(u.new.n)
      mut[TRACKTOT] = str(u.new.t)
    elif u.flac is not None:
      mut[u.flac] = str(u.new)
    cfg.verbose and print('%s = %s' % (u.flac, str(u.new)))
  else:
    raise TypeError('Unknown type: %s' % type(mut))





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                     BUILD QUERY FUNCTIONS                      ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Приоритет установки тегов, если указано несколько источников
# 1. Наивысший приоритет — указание явно
# 2. Автоматическое подсчитывание (номер трека, всего треков)
# 3. Данные из названия файла, имени родительской директории
def make_query(file, number, total):
  q     = Query()
  q.mut = confirm_interface(file, q.mut)
  q.old = meta_from_file(file, q.mut)
  q.new = deepcopy(q.old)

  if cfg.parsefilename: add_tags_from_filename(q.new, file)
  if cfg.numerate:      q.new.track.n   = number
  if cfg.totalauto:     q.new.track.t   = total
  if cfg.artdir:        q.new.artist    = basename(abspath(cfg.dir))
  if cfg.albartdir:     q.new.albartist = basename(abspath(cfg.dir))
  if cfg.albdir:        q.new.album     = basename(abspath(cfg.dir))

  add_tags_from_arguments(q.new)

  if cfg.addgenres:
    q.new.genre.g = (remove_duplicates(
      (q.new.genre.g or []) + cfg.addgenres
    ))

  cfg.sortgenres and q.new.genre.g.sort()

  return q



def add_tags_from_filename(meta, file: str):
  m = re.match(cfg.nameex, basename(file.replace('_', ' ')))
  if m is None:
    raise ValueError('Can\'t parse name of file "%s"' % file)

  if m.group(1) is not None: meta.track.n = int(m.group(1))
  if m.group(2) is not None: meta.artist  = m.group(2)
  if m.group(3) is not None: meta.name    = m.group(3)
  if m.group(2) is not None and cfg.sameartist: meta.albartist = m.group(2)
  if m.group(2) is not None and cfg.samealbum:  meta.album     = m.group(2)



def add_tags_from_arguments(m):
  m.name      = cfg.name      if cfg.name      is not None else m.name
  m.track.n   = cfg.tracknum  if cfg.tracknum  is not None else m.track.n
  m.track.t   = cfg.tracktot  if cfg.tracktot  is not None else m.track.t
  m.artist    = cfg.artist    if cfg.artist    is not None else m.artist
  m.albartist = cfg.albartist if cfg.albartist is not None else m.albartist
  m.album     = cfg.album     if cfg.album     is not None else m.album
  m.genre.g   = cfg.genre     if cfg.genre     is not None else m.genre.g
  m.playcnt   = cfg.playcnt   if cfg.playcnt   is not None else m.playcnt
  m.year      = cfg.year      if cfg.year      is not None else m.year
  m.cd        = cfg.cd        if cfg.cd        is not None else m.cd
  m.comment   = cfg.comment   if cfg.comment   is not None else m.comment





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             CONFIG                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def set_config(args):
  global cfg
  cfg           = args
  cfg.agendels  = ALLOWED_GENDELS
  cfg.nameex    = re.compile(r'^(?:(\d+)\.)?\s*(.+)\s*[ _][-—][ _]\s*(.+)\.(mp3|flac)$')
  cfg.setcom    = 'id3v2 -2 --%s "%s" "%s"'
  cfg.remcom    = 'id3v2 -r "%s" "%s"'
  cfg.tracknum  = int(cfg.tracknum) if cfg.tracknum is not None else None
  cfg.tracktot  = int(cfg.tracktot) if cfg.tracktot is not None else None
  cfg.addgenres = str2genre(cfg.addgenres)
  cfg.genre     = str2genre(cfg.genre)
  cfg.files     = ( args.files if len(args.files) != 0 else
    list(map(lambda x: join(cfg.dir, x),
    [ f for f in listdir(cfg.dir) if re.match(r'.*\.(mp3|flac)', f) ])) )





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                              MAIN                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def main():
  ret = 0
  set_config(make_parser().parse_args())

  cfg.verbose and print()

  for i in range(len(cfg.files)):
    file = cfg.files[i]

    cfg.verbose and print('File \'%s\'' % file)

    try:
      q = make_query(file, i+1, len(cfg.files))
      process_query(q, file)
      q.mut.save()

    except ValueError as e:
      print(e, file=stderr)
      print('Skip file "%s"' % file, file=stderr)
      ret = 1

    except TypeError:
      print('Unknown file format "%s"' % file, file=stderr)
      ret = 1

    cfg.verbose and print()

  return ret


if __name__ == '__main__':
  exit(main())





# END
