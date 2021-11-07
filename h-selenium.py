import requests
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    reg = r'^.{1,20}$'
    URL = "https://kbp.aero/en/"
    driver = webdriver.Chrome()
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    driver.get(URL)

    wait = WebDriverWait(driver, 4)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'td')))
    tds = driver.find_elements(By.CLASS_NAME, "td")
    for td in tds:
        print(td.text)
    # tds = element.find_elements(By.CLASS_NAME, "td")
    # for td in tds:
    #     print(td.text)

    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "tbody"))
    #     )
    #     tds = element.find_elements(By.CLASS_NAME, "td")
    #     for td in tds:
    #         print(td.text)
    #
    # finally:
    #     driver.quit()



if __name__ == "__main__":
    main()