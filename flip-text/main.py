#!/usr/bin/python3

import sys





# objects
mapping = {
	'а' :  'ɐ',
	'б' :  'ƍ',
	'в' :  'ʚ',
	'г' :  'ɹ',
	'д' :  'ɓ',
	'е' :  'ǝ̤',
	'ё' :  'ǝ',
	'ж' :  'ж',
	'з' :  'ε',
	'и' :  'и̯',
	'й' :  'n',
	'к' :  'ʞ',
	'л' :  'v',
	'м' :  'w',
	'н' :  'н',
	'о' :  'о',
	'п' :  'u',
	'р' :  'd',
	'с' :  'ɔ',
	'т' :  'ɯ',
	'у' :  'ʎ',
	'ф' :  'ȸ',
	'х' :  'х',
	'ц' :  'ǹ',
	'ч' :  'Һ',
	'ш' :  'm',
	'щ' :  'm',
	'ъ' :  'q',
	'ы' :  'qı',
	'ь' :  'q',
	'э' :  'є',
	'ю' :  'ıo',
	'я' :  'ʁ',
	'А' :  'ɐ',
	'Б' :  'ƍ',
	'В' :  'ʚ',
	'Г' :  'ɹ',
	'Д' :  'ɓ',
	'Е' :  'ǝ̤',
	'Ё' :  'ǝ',
	'Ж' :  'ж',
	'З' :  'ε',
	'И' :  'и̯',
	'Й' :  'n',
	'К' :  'ʞ',
	'Л' :  'v',
	'М' :  'w',
	'Н' :  'н',
	'О' :  'о',
	'П' :  'u',
	'Р' :  'd',
	'С' :  'ɔ',
	'Т' :  'ɯ',
	'У' :  'ʎ',
	'Ф' :  'ȸ',
	'Х' :  'х',
	'Ц' :  'ǹ',
	'Ч' :  'Һ',
	'Ш' :  'm',
	'Щ' :  'm',
	'Ъ' :  'q',
	'Ы' :  'q',
	'Ь' :  'q',
	'Э' :  'єı',
	'Ю' :  'ıo',
	'Я' :  'ʁ',
	'a' :  'ɐ',
	'b' :  'q',
	'c' :  'ɔ',
	'd' :  'p',
	'e' :  'ǝ',
	'f' :  'ɟ',
	'g' :  'ƃ',
	'h' :  'ɥ',
	'i' :  'ı',
	'j' :  'ɾ',
	'k' :  'ʞ',
	'l' :  'l',
	'm' :  'ɯ',
	'n' :  'u',
	'o' :  'o',
	'p' :  'd',
	'q' :  'ᕹ',
	'r' :  'ɹ',
	's' :  's',
	't' :  'ʇ',
	'u' :  'n',
	'v' :  'ʌ',
	'w' :  'ʍ',
	'x' :  'x',
	'y' :  'ʎ',
	'z' :  'z',
	'A' :  'ɐ',
	'B' :  'q',
	'C' :  'ɔ',
	'D' :  'p',
	'E' :  'ǝ',
	'F' :  'ɟ',
	'G' :  'ƃ',
	'H' :  'ɥ',
	'I' :  'ı',
	'J' :  'ɾ',
	'K' :  'ʞ',
	'L' :  'l',
	'M' :  'ɯ',
	'N' :  'u',
	'O' :  'o',
	'P' :  'd',
	'Q' :  'ᕹ',
	'R' :  'ɹ',
	'S' :  's',
	'T' :  'ʇ',
	'U' :  'n',
	'V' :  'ʌ',
	'W' :  'ʍ',
	'X' :  'x',
	'Y' :  'ʎ',
	'Z' :  'z',
	'!' :  '¡',
	'*' :  '*',
	'(' :  ')',
	')' :  '(',
	'-' :  '-',
	'=' :  '=',
	'_' :  '‾',
	'+' :  '+',
	'[' :  ']',
	']' :  '[',
	'{' :  '}',
	'}' :  '{',
	';' :  ';',
	'?' :  '¿',
	',' :  '‘',
	'.' :  '˙',
	'<' :  '>',
	'>' :  '<',
	'/' :  '\\',
	'\\' : '/',
}
   




# functions
def flat_text(s: str):
	'''
	remove double spaces and replace
	\n and \t to spaces
	'''
	res = ""
	prev_is_space = True

	for sym in s:
		if not sym.isspace():
			prev_is_space = False
			res += sym
			continue

		if not prev_is_space:
			prev_is_space = True
			res += ' ' # replace \n and \t to ' '
			continue

	return res.strip()





# main
text = sys.stdin.read()
text = flat_text(text)
text = ''.join(map(lambda s: mapping.get(s, s), text))[::-1]

print(text)





# END