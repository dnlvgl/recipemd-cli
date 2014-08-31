from bs4 import BeautifulSoup
import urllib

# implement argparse

url = 'http://www.chefkoch.de/rezepte/1616691268862802/Zucchini-Lasagne.html'
page = urllib.urlopen(url)
soup = BeautifulSoup(page.read())

#title
title_ws = soup.find('h1', attrs={'class':'page-title'}).text
title = title_ws.replace(' ', '') # remove whitespace

# ingredients
data = []
table = soup.find('table', attrs={'class':'incredients'})
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # get rid of empty values

# instructions
instructions = soup.find('div', attrs={'id':'rezept-zubereitung'}).text # only get text

# write to file
with open(title.lower() + '.md', 'w') as f: # use title of site as name for file
    f.write('# ' + title  + u'\n' + u'\n')
    f.write('## Zutaten' + u'\n' + u'\n')
    for inner_list in data:
        f.write('- ' + ' '.join(inner_list).encode('utf-8') + '\n')
        # data = list of lists; join inner lists
    f.write(u'\n' + u'\n' + '## Zubereitung' + u'\n' + u'\n')
    f.write((instructions.strip()).encode('utf-8')) #.strip() to remove leadin and ending whitespace
    f.write('\n\n[Quelle](' + url + ')')
