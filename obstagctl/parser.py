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
		'file',
		type = str,
		help = 'Файл или директория для обработки'
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
def get_files(args) -> [ str ]:
	'''
	Получает все файлы, которые требуют обработки
	в соответствии с аргументами командной строки.
	'''
	files = []

	# args
	if os.path.isfile(args.file):
		return [ args.file ]

	if not os.path.isdir(args.file):
		raise Exception('Файл "%s" не существует' % args.file)

	if args.recursive:
		recursive(
			args.file,
			lambda f: files.append(f),
			onlyfiles=True )
	else:
		for fname in os.listdir(args.file):
			fname = os.path.join(args.file, fname)
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
	# Может выкинуть исключение
	tagmap = eval(map)

	tmp = {}
	for key, value in tagmap.items():
		if not isinstance(key, str) or not isinstance(value, str):
			raise Exception("Элементы отображения должны быть строками")

		if len(key) > 0 and key[0] != '#':
			key = '#' + key
		if len(value) > 0 and value[0] != '#':
			value = '#' + value

		tmp[key] = value

	return tmp





# END
