from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    reg = r'^.{1,20}$'
    driver = webdriver.Chrome()
    driver.get("https://kbp.aero/en/")

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'td'), ''))

    print(element)
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