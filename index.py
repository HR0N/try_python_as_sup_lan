from bs4 import BeautifulSoup
import requests

def parse():
    URL = 'https://www.klo.ua/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'general-price-item')
    comps = []
    for item in items:
        comps.append({
            'title':item.find('div', class_ = 'general-price-item__title').get_text(strip = True),
            'value':item.find('div', class_ = 'general-price-item__value').get_text(strip = True),
            'value':item.find('div', class_ = 'general-price-item__value').get_text(strip = True),
        })
    for comp in comps:
        print(comp['title'], ' - ', comp['value'])
    # for item in items:
    #     comps.append({
    #         'text': item.get_text(strip=True)
    #     })
    #
    # for comp in comps:
    #     print(comp['text'])

parse()