import re

from bs4 import BeautifulSoup
import json
from selenium import webdriver


URL = "https://kbp.aero/en/"
driver = webdriver.Chrome()
driver.get(URL)
soup = BeautifulSoup(driver.page_source)
json = json.dumps(str(soup))
first = 'https://kbp.aero/wp-content/themes/'
pattern = r"https://kbp.aero/wp-content/themes/borispol-magenta/js/board.js(.){18}"
result = re.search(pattern, json)
print(result.group())

