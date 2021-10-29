#!/usr/bin/python3

import bs4
import re
import requests as req
import os
import time

from sys import exit






########################### GLOBAL OBJECTS ###########################

site   = 'https://www.asciiart.eu'
trgdir = './arts'
failhtml = None





########################### PARSE FUNCTIONS ##########################

def get_html(url, limit: int = 3000):
	global failhtml

	for i in range(10):
		text = req.get(url).text
		if len(text) >= limit:
			return text
		failhtml = text
		print("Can\t get html (%i), sleep for 0.5 second" % i, flush=True)
		time.sleep(0.5)
	raise Exception('Can\'t get html ten times at one attempt')



def parse_ascii_page(text: str):
	arts = []
	for it in re.finditer(r'<pre class="[^"]*">', text):
		arts.append(text[it.end():text.find('</pre>', it.end())])

	return arts



def parse_category_conttable(text: str, cat: str):
	soup = bs4.BeautifulSoup(text, 'lxml')
	refs = soup.find_all('a')

	refs = filter(lambda t:
		t.has_attr('href')              and
		t['href'].startswith('/' + cat) and
		t['href'] != '/' + cat,
	refs)

	res = []
	for ref in refs:
		if ref.text.strip()[-1] != '@':
			res.append(ref['href'][1:])
			continue
		text     = get_html(site + ref['href'])
		subrefs  = parse_category_conttable(text, ref['href'][1:])
		res     += subrefs

	return res



def parse_main_conttable(text: str):
	soup = bs4.BeautifulSoup(text, 'lxml')
	div  = soup.find(class_='directory-columns')
	lst  = div.ul.find_all('li')
	return list(map(lambda t: t.a['href'][1:], lst))





########################### HELP FUNCTIONS ###########################

def mkdirs(root, dirs):
	for dir in dirs:
		try:    os.makedirs(os.path.join(root, dir))
		except: pass





################################ MAIN ################################

def main():
	text = get_html(site)
	cats = parse_main_conttable(text) # categories
	mkdirs(trgdir, cats)

	for cat in cats:
		text = get_html(site + '/' + cat)
		refs = parse_category_conttable(text, cat)
		print('\nCategory: %s\n' % cat, flush=True)
		mkdirs(trgdir, refs)

		for ref in refs:
			refd = os.path.join(trgdir, ref)
			print(refd, flush=True)
			text = get_html('/'.join([site, ref]))
			arts = parse_ascii_page(text)

			for i in range(len(arts)):
				with open('%s/%03i.txt' % (refd, i), 'w') as file:
					file.write(arts[i])

		print('\n', flush=True)

	return 0



if __name__ == '__main__':
	exit(main())





# END
