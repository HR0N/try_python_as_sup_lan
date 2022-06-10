from selenium import webdriver
driver = webdriver.Chrome("chromedriver.exe")


def gmail_login():
    driver.get("https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser")
    driver.find_element_by_name("identifier").send_keys("minecraftbastion2")
    driver.find_element_by_xpath("//*[@id='identifierNext']/div/button/span").click()
    driver.implicitly_wait(5)
    driver.find_element_by_name("password").send_keys("examplepass123")
    driver.find_element_by_xpath("//*[@id='passwordNext']/div/button/span").click()


gmail_login()