# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import html
import requests
import re


# # Read in a page
# html = scraperwiki.scrape("https://www.critrolestats.com/dmcrits-wm")  
## need everything in the <ol> elements with class c6

##root = fromstring(page.content)
##print [child.tag for child in root.iterdescendants()]


page4 = requests.get('https://docs.google.com/document/d/e/2PACX-1vTUFPPB_-rNgpVkDe-F23ADUyggxuTGPO2t15Wg94PGipS39QFxLEQF7WmN0UkSm4mUrVA2_ZYankSD/pub?embedded=true')
#tree4 = html.fromstring(page4.content)

from lxml.html.soupparser import fromstring
root = fromstring(page4.content)


dat = {'character': '', 'episode_info': '', 'killed_what': '', 'kills': 0, 'details': '', 'pk': 0}
scraperwiki.sqlite.save(unique_keys=['pk'], data = dat)


pk = 1
for element in root.body.getchildren():
    if element.tag == 'h3':
        episode = element[0].text
        if element.getnext().tag == 'ol':
            for l in element.getnext():
                k = l[0].text
                ind = k.find('(')
                char = k[0:ind-1]
                ind2 = k.find(')')
                epinfo = k[ind+1:ind2]
                killedwhat = k[ind2+2:len(k)]
                if char.find(',') > -1:
                    ch = char.split(',')
                    for c in ch:
                        char = c.replace(' and ','').strip()
                        dat = {'character': char, 'episode_info': episode, 'killed_what': killedwhat, 'kills': 1.0/len(ch), 'details': k, 'pk': pk}
                        scraperwiki.sqlite.save(unique_keys=['pk'], data = dat)
                        pk += 1
                elif char.find(',') == -1 and char.find(' and ') > -1:
                    ch = char.split(' and ')
                    for c in ch:
                        char = c.strip()
                        dat = {'character': char, 'episode_info': episode, 'killed_what': killedwhat, 'kills': 1.0/len(ch), 'details': k, 'pk': pk}
                        scraperwiki.sqlite.save(unique_keys=['pk'], data = dat)
                        pk += 1
                else:
                    dat = {'character': char, 'episode_info': episode, 'killed_what': killedwhat, 'kills': 1.0, 'details': k, 'pk': pk}
                    scraperwiki.sqlite.save(unique_keys=['pk'], data = dat)
                    pk += 1

        


#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("ol[class='c6']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
