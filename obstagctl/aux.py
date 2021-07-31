import os





# functions
def recursive(root, fun, onlyfiles=False, onlydirs=False):
	'''
	Проходит по всем файлам и директориям внутри заданной
	корневой папки рекурсивно и для каждого файла и директории
	вызывает функцию fun; если установлен флаг onlyfiles, то
	функция вызывается только для файлов, если же onlydirs, то
	только для директорий. В функцию передаётся имя файла.
	'''
	for name in os.listdir(root):
		name   = os.path.join(root, name)
		isfile = os.path.isfile(name)

		if (
			(not onlyfiles and not onlydirs) or
			(    onlyfiles and     isfile)   or
			(    onlydirs  and not isfile)
		):
			fun(name)

		if os.path.isdir(name):
			recursive(name, fun, onlyfiles, onlydirs)
	return





# END
