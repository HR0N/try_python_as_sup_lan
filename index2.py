from bs4 import BeautifulSoup
import requests
import time

def parse():
    URL = 'https://kbp.aero/ru/glavnaya/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    time.sleep(1)
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', class_ = 'table_wrp out yesterday')
    items = items.findAll('tr', class_ = 'tr')
    comps = []
    if(len(items) > 0):
        for item in items:
            comps.append({
                'title':item.find('td', class_ = 'td').get_text(strip = True),
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

