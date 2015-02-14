#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import codecs
import sys


def chefkoch(soup):
    # title
    title = soup.find('h1', attrs={'class': 'page-title'}).text.replace(' ', '')
    # ingredients
    ingreds = []
    table = soup.find('table', attrs={'class': 'incredients'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        ingreds.append([ele for ele in cols if ele])  # get rid of empty values
    # instructions
    instruct = soup.find('div', attrs={'id': 'rezept-zubereitung'}).text  # only get text
    # write to file
    with codecs.open(title.lower() + '.md', 'w', encoding="utf-8") as f:  # title = filename
        f.write('# ' + title + '\n\n')
        f.write('## Zutaten' + '\n\n')
        for inner_list in ingreds:
            f.write('- ' + ' '.join(inner_list) + '\n')
            # data = list of lists; join inner lists
        f.write('\n\n' + '## Zubereitung' + '\n\n')
        f.write(instruct.strip())  # .strip() to remove leadin and ending whitespace


def allrecipes(soup):
    # title
    title = soup.find('h1', attrs={'id':'itemTitle'}).text
    # ingredients
    ingreds = soup.find('div', attrs={'class': 'ingred-left'})
    ingreds = [s.getText().strip() for s in ingreds.findAll('li')]
    ingreds = ['- ' + s.replace('\n', ' ') for s in ingreds] #add dash + remove newlines
    # instructions
    instruct = soup.find('div', attrs={'class':'directLeft'})
    instruct = [s.getText().strip() for s in instruct.findAll('li')]
    # write to file
    with open(title.lower().replace(' ', '-') + '.md', 'w') as f:
        f.write('# ' + title + '\n\n')
        f.write('## Zutaten' + '\n\n')
        f.write('\n'.join(ingreds))
        f.write('\n\n' + '## Zubereitung' + '\n\n')
        f.write(' '.join(instruct))


def main():
    url = sys.argv[1]
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page.read())

    if url.startswith('http://www.chefkoch.de/'):
        chefkoch(soup)
    elif url.startswith('http://allrecipes.com/'):
        allrecipes(soup)
    else:
        print 'nope'


if __name__ == "__main__":
    main()
