#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import codecs
import sys

# implement argparse

url = sys.argv[1]
page = urllib.urlopen(url)
soup = BeautifulSoup(page.read())

#title
title = soup.find('h1', attrs={'class':'page-title'}).text

# ingredients
ingreds = []
table = soup.find('table', attrs={'class':'incredients'})
rows = table.find_all('tr')
for row in rows:
	cols = row.find_all('td')
	cols = [ele.text.strip() for ele in cols]
	ingreds.append([ele for ele in cols if ele]) # get rid of empty values
# instructions
instruct = soup.find('div', attrs={'id':'rezept-zubereitung'}).text # only get text
# write to file
with codecs.open(title.lower() + '.md', 'w', encoding="utf-8") as f: # use title of site as name for file
	f.write('# ' + title + '\n\n')
	f.write('## Zutaten' + '\n\n')
	for inner_list in ingreds:
	    f.write('- ' + ' '.join(inner_list) + '\n')
	    # data = list of lists; join inner lists
	f.write('\n\n' + '## Zubereitung' + '\n\n')
	f.write(instruct.strip()) #.strip() to remove leadin and ending whitespace
