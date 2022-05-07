from mysql.connector import Error
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import requests
import random
import time

# todo:                                             ..:: variables ::..
driver = webdriver.Chrome("chromedriver.exe")
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                      "Chrome/95.0.4638.69 Safari/537.36")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.headless = True
# driver = webdriver.Chrome(
#     executable_path="chromedriver.exe",
#     options=options
# )
parse_interval = 120
rand = random.randint(2, 5)
all_data = []

# todo:                                             ..:: code ::..


def gmail_login():
    driver.get(
        "https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail."
        "google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser")
    driver.implicitly_wait(rand)
    driver.find_element_by_name("identifier").send_keys("work.it.des")
    driver.find_element_by_xpath("//*[@id='identifierNext']/div/button/span").click()
    driver.implicitly_wait(5)
    driver.find_element_by_name("password").send_keys("qwerty0123456789gmail")
    driver.find_element_by_xpath("//*[@id='passwordNext']/div/button/span").click()
    driver.implicitly_wait(rand)


def kaban_login():
    driver.get("https://kabanchik.ua/cabinet/dashboard/p/recommended")
    driver.implicitly_wait(rand)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/div/div/div[1]/div/div/form/div[1]/div/div/div[1]/a").click()
    driver.implicitly_wait(5)


def kaban_linking():
    driver.get("https://kabanchik.ua/cabinet/dashboard/p/recommended")
    time.sleep(1)
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
    global all_data
    kaban_data: list = []
    URL = 'https://kabanchik.ua/cabinet/dashboard/p/recommended'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    # soup = BeautifulSoup(response.content, 'html.parser')
    html = html_catch
    soup = BeautifulSoup(html)

    number = soup.find('span', class_='kb-task-details__task-id').get_text(strip=True)
    kaban_data.append(number)

    name = soup.find('h1', class_='kb-task-details__title').get_text(strip=True)
    name = name.split("№")[0]
    kaban_data.append(name)

    price = soup.find('span', class_='js-task-cost').get_text(strip=True)
    kaban_data.append(price)

    deadline = soup.find('span', class_='js-datetime_due').get_text(strip=True)
    kaban_data.append(deadline)

    tasks = soup.findAll('div', class_='kb-task-details__non-numeric-attribute')
    tasks_data: list = []
    sTasks: str = '(^_^)'
    for task in tasks:
        tasks_data.append(task.get_text(strip=True))
    sTasks = sTasks.join(tasks_data)
    sTasks = sTasks.replace('(^_^)', '\n')
    if len(sTasks) < 5:
        sTasks = 'Без ТЗ.'
    kaban_data.append(sTasks)

    comment = soup.find('div', attrs={'data-bazooka': 'LinkifyText'}).get_text(strip=True)
    kaban_data.append(comment)

    client = soup.find('a', class_='kb-sidebar-profile__name').get_text(strip=True)
    kaban_data.append(client)

    review = soup.find('span', class_='kb-sidebar-profile__reviews-count').get_text(strip=True)
    kaban_data.append(review)

    positive = soup.find('div', class_='kb-sidebar-profile__rating').get_text(strip=True)
    kaban_data.append(positive)

    yes_in = False
    for item in all_data:
        if name in item:
            yes_in = True
            break
    if not yes_in:
        insert_data(kaban_data)
        message = '<b>' + name + '</b>\n<b>' + price + '</b> \n\nDeadline: ' + deadline + '\n\n<b>ТЗ: </b>\n' \
                  '' + sTasks + '\n\n<b>Комментарий: </b> ' + comment + '\n\n<b>Клиент: </b> ' + client + ' ' \
                  '\n' + review + ' - ' + positive + \
                  '\n========================='
        send_telegram(message)
        time.sleep(.5)
        get_data()
        time.sleep(.5)
    print(kaban_data)


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="pr435071.mysql.tools",
            user="pr435071_parsehub",
            passwd="y5f3VS*~2r",
            database="pr435071_parsehub"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def get_data():
    global all_data
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = (
        "SELECT * FROM `kabanchik2` WHERE 1")
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()
    all_data = records
    return records


def get_names():
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = (
        "SELECT `name` FROM `kabanchik2` WHERE 1")
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()
    return records


def insert_data(coming_data):
    connection = create_connection()
    cursor = connection.cursor()
    sqlData = coming_data
    sql = (
        "INSERT INTO kabanchik2 ( number, name, price, deadline, tasks, comment, client, review, positive )"
        "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, sqlData)
    cursor.close()


# todo:                                         .. :: Telegram :: ..
def send_telegram(tmessage: str):
    token = "5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4"
    channel_id = "-692711290"
    url2 = 'https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+channel_id+'&parse_mode=' \
                                                                                   'html&text='+tmessage
    r = requests.post(url2)

    if r.status_code != 200:
        raise Exception("post_text error")


# todo:                                         .. :: Drive Me Baby :: ..

gmail_login()
time.sleep(25)

kaban_login()
get_data()
driver.implicitly_wait(3)
time.sleep(rand)

kaban_linking()
driver.implicitly_wait(3)
time.sleep(rand)