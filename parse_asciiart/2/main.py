#!/usr/bin/python3

import re
import requests as req
import os
import time

from bs4 import BeautifulSoup as BS
from sys import exit, stderr





########################### GLOBAL OBJECTS ###########################
site     = 'http://www.ascii-art.de/ascii'
trgdir   = './arts'
failhtml = None
pages    = [
	'http://www.ascii-art.de/ascii/index.shtml',
	'http://www.ascii-art.de/ascii/index_c.shtml',
	'http://www.ascii-art.de/ascii/index_def.shtml',
	'http://www.ascii-art.de/ascii/index_ghi.shtml',
	'http://www.ascii-art.de/ascii/index_jkl.shtml',
	'http://www.ascii-art.de/ascii/index_mno.shtml',
	'http://www.ascii-art.de/ascii/index_pqr.shtml',
	'http://www.ascii-art.de/ascii/index_s.shtml',
	'http://www.ascii-art.de/ascii/index_t.shtml',
	'http://www.ascii-art.de/ascii/index_uvw.shtml',
	'http://www.ascii-art.de/ascii/index_xyz.shtml',
]





########################### PARSE FUNCTIONS ##########################

def get_html(url, limit: int = 3000):
	global failhtml

	for i in range(10):
		text = req.get(url).text
		if len(text) >= limit:
			return text
		failhtml = text
		if i == 0:
			print('html: %s' % url)
		print("Can\t get html (%i), sleep for 0.5 second" % i, flush=True)
		time.sleep(0.5)
	raise Exception('Can\'t get html ten times at one attempt')



def parse_conttable_page(text: str):
	soup = BS(text, 'lxml')
	refs = soup.find_all(lambda t:
		t.has_attr('class') and t.has_attr('href') and
		('c1' in t['class'] or 'c2' in t['class'])
	)
	return list(map(lambda t: t['href'], refs))





################################ MAIN ################################

def main():
	try:    os.makedirs(trgdir)
	except: pass

	for url in pages:
		text = get_html(url)
		refs = parse_conttable_page(text)

		print("Content table: %s" % url, flush=True)
		for ref in refs:
			try:
				text = get_html(site + '/' + ref, 0)
			except:
				print("ERROR, skip page %s" % ref, flush=True, file=stderr)
				continue

			print(ref, flush=True)
			try:
				name = re.search(r'/([^./]+\.txt)', ref).group(1)
				open(os.path.join(trgdir, name), 'w').write(text)
			except:
				print("Error, skip %s" % ref)

	return 0



if __name__ == '__main__':
	exit(main())





# END
