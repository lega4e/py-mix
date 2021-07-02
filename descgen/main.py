#!/usr/bin/python3





######################## PARAMETRES ########################
inpseps       = ' \t' # символы, отделяющие значения от описаний на входе

linewidth     = 80    # длина всей линии
desclinewidth = -1    # длина описания
outdescbegin  = '#'   # символ, который будет разделять значение и описание
outspace      = 1     # количество outsep
emptyline     = True  # будет ли вставляться пустая строка между значениями





######################### FUNCTIONS ########################
def find_if(iter, fun):
	i = 0
	for val in iter:
		if fun(val):
			return i, val
		i += 1
	return -1, None


def split_string(s : str, l : int) -> [ str ]:
	words = s.split(' ')
	lines = []

	if len(words) == 0:
		return lines

	wordi = 0
	line  = ''
	while wordi < len(words):
		if len(line) + len(words[wordi]) + 1 <= l or len(line) == 0:
			line += words[wordi] + ' '
			wordi += 1
		else:
			lines.append(line[:-1])
			line = ''
	lines.append(line[:-1])

	return lines;





########################### MAIN ###########################
items       = []
valuemaxlen = 0

# read
while True:
	try:             line = input()
	except EOFError: break

	found = list(filter(lambda x: x >= 0, [line.find(sep) for sep in inpseps]))
	p     = min(found) if len(found) != 0 else len(line)

	value = line[:p].strip()
	valuemaxlen = max(valuemaxlen, len(value))

	for p in range(p, len(line)):
		if line[p] not in inpseps:
			break
	desc = line[p:].strip()

	items.append((value, desc))



# transform
for i in range(len(items)):
	value, desc = items[i]
	desc = split_string(
		desc,
		desclinewidth if desclinewidth > 0 else
		linewidth - valuemaxlen - 2 - len(outdescbegin)
	)

	lines = []
	line = ''
	if len(value) != 0:
		line  = value + ' ' * (valuemaxlen - len(value) + outspace)
		line += outdescbegin + ' ' + desc[0]
	lines.append(line)

	for descline in desc[1:]:
		line  = ' ' * (valuemaxlen + outspace)
		line += outdescbegin + ' ' + descline
		lines.append(line)

	items[i] = lines



# write
for lines in items:
	if len(lines) == 1 and len(lines[0]) == 0:
		print()
	else:
		print(*lines, sep='\n', end='\n\n' if emptyline else '\n')





# END
