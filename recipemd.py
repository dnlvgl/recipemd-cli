#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import codecs
import sys


def chefkoch(soup):
    # title
    title = soup.find('h1', attrs={'class': 'page-title'}).text
    # ingredients
    ingreds = []
    table = soup.find('table', attrs={'class': 'incredients'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [s.text.strip() for s in cols]
        ingreds.append([ele for ele in cols if ele])  # get rid of empty values
    ingreds = ['- ' + ' '.join(s) for s in ingreds]
    # instructions
    instruct = soup.find('div', attrs={'id': 'rezept-zubereitung'}).text  # only get text
    instruct = instruct.strip()  # remove leadin and ending whitespace
    # write to file
    writeFile(title, ingreds, instruct)


def allrecipes(soup):
    # title
    title = soup.find('h1', attrs={'id': 'itemTitle'}).text
    # ingredients
    ingreds = soup.find('div', attrs={'class': 'ingred-left'})
    ingreds = [s.getText().strip() for s in ingreds.findAll('li')]
    ingreds = ['- ' + s.replace('\n', ' ') for s in ingreds]  # add dash + remove newlines
    ingreds = [" ".join(s.split()) for s in ingreds]  # remove whitespace
    # instructions
    instruct = soup.find('div', attrs={'class': 'directLeft'})
    instruct = [s.getText().strip() for s in instruct.findAll('li')]
    instruct = '\n\n'.join(instruct)
    # write to file
    writeFile(title, ingreds, instruct)


def writeFile(title, ingreds, instruct):
        with codecs.open(title.lower().replace(' ', '-') + '.md', 'w', encoding="utf-8") as f:
            f.write('# ' + title + '\n\n')
            f.write('## Zutaten' + '\n\n')
            f.write('\n'.join(ingreds))
            f.write('\n\n' + '## Zubereitung' + '\n\n')
            f.write(instruct)


def main():
    url = sys.argv[1]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html5lib")

    if url.startswith('http://www.chefkoch.de/'):
        chefkoch(soup)
    elif url.startswith('http://allrecipes.com/'):
        allrecipes(soup)
    else:
        print ('nope')


if __name__ == "__main__":
    main()