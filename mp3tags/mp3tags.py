#!/usr/bin/python3
import os
import re
import sys



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                             fields                             ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
tmpl = re.compile(r'^(?:(\d+)\.)?\s*(.*)\s* - \s*(.*)\.mp3$')

album  = 'Избранное'
com    = 'id3v2 --%s "%s" "%s"'
fields = [
	( 'TRCK', lambda m: m.group(1) ), # Номер трека
	( 'TALB', lambda m: album      ), # Альбом
	( 'TPE1', lambda m: m.group(2) ), # Исполнитель
	( 'TPE2', lambda m: m.group(2) ), # Исполнитель альбома
	( 'TIT2', lambda m: m.group(3) ), # Название
]



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~                              main                              ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():
	ret   = 0
	files = [ file for file in os.listdir() if re.match(r'.*\.mp3', file) ]

	for file in files:
		m = re.match(tmpl, file)

		if m is None:
			print("Error: invalid name of file %s" % file, file=sys.stderr)
			ret = 1
			continue

		for flag, getval in fields:
			thecom = com % (flag, getval(m) or '', file)
			print(thecom)
			os.system(thecom)

		print()

	return ret

if __name__ == '__main__':
	exit(main())



# END
