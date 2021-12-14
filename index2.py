#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
import requests

print('test')
def parse():
    URL = 'https://index.minfin.com.ua/markets/fuel/tm/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('table', class_='zebra')
    # items = items.findAll('tr', class_ = 'tr')
    items = items.findAll('tr')
    comps = []
    items2 = str(items)
    items2 = json.dumps(items2)
    if(len(items) > 0):
        for item in items:
            comps.append({
                'title': item.find('a').get_text(strip=True),
            })
            if(item.find('td', class_='r1')):
                comps.append({
                    'title': item.find('td', class_='r1').get_text(strip=True),
                })
        # for item in items:
        #     comps.append({
        #         'text': item.get_text(strip=True)
        #     })
    # for comp in comps:
    #     print(comp['title'])
    print(items2)



parse()
