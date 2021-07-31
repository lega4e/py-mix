import re





# objects
tag_re    = re.compile(r'#[\w_]+')
code_re   = re.compile(r'```')
incode_re = re.compile(r'`')





# help functions
def contains(inters, val) -> bool:
	'''
	Проверяет, находится ли значение в одном из отрезков inters. 
	'''
	for inter in inters:
		if inter[0] <= val <= inter[1]:
			return True
	return False





# core
def tag_iter(data: str):
	'''
	Итерируемый объект, с помощью которого можно пройтись
	по всем тегам в тексте. Теги определяются с помощью
	регулярного выражения tag_re. На каждой итерации
	возвращается объект-совпадение (match), соответствующий
	регулярному выражению тега. Из рассмотрения исключаются
	теги, которые попадают в скобки '```' или '`'.
	'''
	inters = [ edge.span()[0] for edge in re.finditer(code_re, data) ]
	if len(inters) % 2 == 1:
		inters.append(len(data))
	inters = [ (inters[i], inters[i+1]) for i in range(0, len(inters), 2) ]

	inline = [ edge.span()[0] for edge in re.finditer(incode_re, data) ]
	inline = list(filter(lambda x: not contains(inters, x), inline))
	if len(inline) % 2 == 1:
		inline.append(len(data))
	inline = [ (inline[i], inline[i+1]) for i in range(0, len(inline), 2) ]

	inters.extend(inline)

	for tag in re.finditer(tag_re, data):
		if contains(inters, tag.span()[0]) or contains(inters, tag.span()[1]):
			continue

		yield tag


def replace_tags_in_string(data: str, repmap: { str : str }) -> str:
	'''
	Заменяет все теги в тексте в соответствии с отображением
	(если тега в отображении нет, то он остаётся неизменным).
	'''
	pos = 0
	res = ''
	for tag in tag_iter(data):
		res += data[pos:tag.span()[0]]
		res += repmap.get(tag.group(0), tag.group(0))
		pos  = tag.span()[1]

	res += data[pos:]
	return res





# END
