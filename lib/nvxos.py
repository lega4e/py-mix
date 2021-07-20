import os





def recursive(root, fun, onlyfiles=False):
	for file in os.listdir(root):
		file = os.path.join(root, file)
		if not onlyfiles or os.path.isfile(file):
			fun(file)
		if os.path.isdir(file):
			recursive(file, fun)
	return





# END
