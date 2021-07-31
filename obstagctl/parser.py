import argparse
import os

from aux import recursive





############################################################
# init parser
def create_parser():
	'''
	Создаёт парсер аргументов командной строки
	'''
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
	'''
	Получает все файлы, которые требуют обработки
	в соответствии с аргументами командной строки.
	'''
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
				if os.path.isfile(fname):
					files.append(fname)

	if not args.nomdonly:
		files = list(filter(lambda f: len(f) > 2 and f[-2:] == 'md', files))

	return files



def read_tagmap(map: str) -> { str : str }:
	'''
	Преобразует строку в отображение одних тегов в другие;
	строка должна иметь тот же формат, с помощью которго
	в питоне задаётся словарь, например, "{ 'one' : 'another' }"
	'''
	try:
		tagmap = eval(map)
	except Exception as e:
		print('Error: ' + str(e), file=sys.stderr)
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





# END
