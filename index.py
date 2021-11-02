from bs4 import BeautifulSoup
import requests

def parse():
    URL = 'https://kbp.aero/ru/glavnaya/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', class_ = 'another-wrapper-for-all-pages-because-trulala home')
    comps = []
    # for item in items:
    #     comps.append({
    #         'title': item.find('tr', class_ = 'tr').get_text(strip = True)
    #     })
    #     for comp in comps:
    #         print(comp['title'])
    print(items)
    # for item in items:
    #     comps.append({
    #         'text': item.get_text(strip=True)
    #     })
    #
    # for comp in comps:
    #     print(comp['text'])

parse()