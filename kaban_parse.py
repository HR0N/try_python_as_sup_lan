from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")
import requests
import mysql.connector
import time
from mysql.connector import Error
import random

# todo:                                             ..:: variables ::..
parse_interval = 120
rand = random.randint(2, 5)

# todo:                                             ..:: code ::..

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=.\User')
options.add_argument('--profile-directory=Profile 1')


def gmail_login():
    driver.get(
        "https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser")
    driver.find_element_by_name("identifier").send_keys("work.it.des")
    driver.find_element_by_xpath("//*[@id='identifierNext']/div/button/span").click()
    driver.implicitly_wait(5)
    driver.find_element_by_name("password").send_keys("qwerty0123456789gmail")
    driver.find_element_by_xpath("//*[@id='passwordNext']/div/button/span").click()


def kaban_login():
    driver.get("https://kabanchik.ua/cabinet/dashboard/p/recommended")
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/div/div/div[1]/div/div/form/div[1]/div/div/div[1]/a").click()
    driver.implicitly_wait(5)


def kaban_linking():
    links = driver.find_elements_by_class_name("kb-dashboard-performer__title")
    driver.implicitly_wait(rand)
    for link in links:
        link.click()
        time.sleep(1)
        cur_handlers = driver.window_handles
        driver.switch_to.window(cur_handlers[1])
        driver.implicitly_wait(2)
        time.sleep(1)
        kaban_parse(driver.page_source)
        time.sleep(rand)
        driver.close()
        driver.implicitly_wait(rand)
        driver.switch_to.window(cur_handlers[0])
        time.sleep(1)


def kaban_parse(html_catch):
    # data = {"number": "", "name": "", "price": "", "deadline": "", "tasks": "", "comment": "", "client": "",
    #         "review": "", "positive": ""}
    data: list = []
    URL = 'https://kabanchik.ua/cabinet/dashboard/p/recommended'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    # soup = BeautifulSoup(response.content, 'html.parser')
    html = html_catch
    soup = BeautifulSoup(html)

    number = soup.find('span', class_='kb-task-details__task-id').get_text(strip=True)
    data.append(number)

    name = soup.find('h1', class_='kb-task-details__title').get_text(strip=True)
    name = name.split("№")[0]
    data.append(name)

    price = soup.find('span', class_='js-task-cost').get_text(strip=True)
    data.append(price)

    deadline = soup.find('span', class_='js-datetime_due').get_text(strip=True)
    data.append(deadline)

    tasks = soup.findAll('div', class_='kb-task-details__non-numeric-attribute')
    tasks_data: list = []
    sTasks: str = ''
    for task in tasks:
        tasks_data.append(task.get_text(strip=True))
    sTasks = sTasks.join(tasks_data)
    data.append(sTasks)

    comment = soup.find('div', attrs={'data-bazooka': 'LinkifyText'}).get_text(strip=True)
    data.append(comment)

    client = soup.find('a', class_='kb-sidebar-profile__name').get_text(strip=True)
    data.append(client)

    review = soup.find('span', class_='kb-sidebar-profile__reviews-count').get_text(strip=True)
    data.append(review)

    positive = soup.find('div', class_='kb-sidebar-profile__rating').get_text(strip=True)
    data.append(positive)

    print(data)

    connection = create_connection("pr435071.mysql.tools", "pr435071_parsehub", "y5f3VS*~2r", "pr435071_parsehub", data)

    # items = soup.findAll('div', class_='kb-dashboard-performer__wrapper')
    # items = soup.find('div', class_='kb-dashboard')
    # items = items.findAll('div', class_='kb-dashboard-performer__wrapper')


def create_connection(host_name, user_name, user_password, db_name, data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    cursor = connection.cursor()
    data_parse = data
    add_parse = (
        "INSERT INTO kabanchik2 ( number, name, price, deadline, tasks, comment, client, review, positive )"
        "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    # add_parse = ("UPDATE weather SET json = ( %s) WHERE id = 1")
    cursor.execute(add_parse, data_parse)

    return connection


# connection = create_connection("pr435071.mysql.tools", "pr435071_parsehub", "y5f3VS*~2r", "pr435071_parsehub")

# todo:                                         .. :: Drive Me Baby :: ..

gmail_login()
driver.implicitly_wait(3)

kaban_login()
driver.implicitly_wait(3)
time.sleep(rand)

kaban_linking()
driver.implicitly_wait(3)
time.sleep(rand)

