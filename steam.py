from bs4 import BeautifulSoup
import requests
import time
import re

def parse():
    URL = 'https://store.steampowered.com/search/?sort_by=Released_DESC&tags=1702%2C492%2C9%2C597%2C19'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    pattern = r'^https://store.steampowered.com/app/'
    items = soup.findAll('a', href=re.compile(pattern))
    comps = []
    if(len(items) > 0):
        for item in items:
            comps.append({
                'title':item.find('span', class_ = 'title').get_text(strip = True),
            })
    for comp in comps:
        print(comp['title'])
    # for item in items:
    #     comps.append({
    #         'text': item.get_text(strip=True)
    #     })
    #
    # for comp in comps:
    #     print(comp['text'])

parse()

