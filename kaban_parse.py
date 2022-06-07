from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector
import requests
import random
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import telebot


# todo:                                         .. :: WebDriver :: ..

ua = UserAgent()
options = Options()
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
driver = webdriver


def start_driver():
    global driver
    driver = webdriver
    driver = driver.Chrome(executable_path=(ChromeDriverManager().install()), options=options)


def stop_driver():
    driver.close()

# driver = webdriver.Chrome(executable_path=(ChromeDriverManager().install()), options=options)
# options.headless = True
# service = Service(ChromeDriverManager().install())            -----for new selenium versions
# driver = webdriver.Chrome(service=service, options=options)   -----for new selenium versions
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# todo:                                             ..:: variables ::..


parse_interval = 120
rand = random.randint(2, 5)
all_data = []
telegram_chat_id = 441246772
state = {
    'write_sms': False,
    'code': 0,
}


bot = telebot.TeleBot("5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4", parse_mode=None)


# todo:                                             ..:: code ::..


def gmail_login():
    print("Gmail Authorization.")
    driver.get(
        "https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail."
        "google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser")
    driver.implicitly_wait(rand)
    driver.find_element(By.NAME, "identifier").send_keys("work.it.des")
    driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button/span").click()
    driver.implicitly_wait(5)
    driver.find_element(By.NAME, "password").send_keys("1qaz@WSX3edc$RFV")
    driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button/span").click()
    driver.implicitly_wait(rand)
    time.sleep(2)
    driver.get_screenshot_as_file('./sms.png')
    print('screen')
    time.sleep(3)
    sXpath = "//*[@id='view_container']/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[1]/"
    isSet = check_exists_by_xpath(sXpath)
    # isSet = len(driver.find_elements(By.XPATH, sVerify)) > 0
    if isSet:
        print('Send verify SMS')
        state['write_sms'] = True
        msg = "Waiting for SMS..."
        bot.send_message(telegram_chat_id, msg)
        driver.find_element(By.XPATH, sXpath).click()
        time.sleep(45)
        driver.get_screenshot_as_file('./smsCode.png')
        print('screen')
        verifyCode = read_code()
        driver.find_element(By.NAME, "idvPin").send_keys(verifyCode)
        time.sleep(2)
        driver.find_element(By.XPATH, "//*[@id='view_container']/div/div/div[2]/div/div[2]/div/div[1]/div/"
                                      "div/button/div[3]").click()
        time.sleep(3)
    driver.implicitly_wait(rand)


def kaban_login():
    print("Kaban4ik Authorization.")
    driver.get("https://kabanchik.ua/cabinet/dashboard/p/recommended")
    driver.implicitly_wait(rand)
    driver.find_element(By.XPATH
                        , "/html/body/div[2]/div[2]/div/div/div/div[1]/div/div/form/div[1]/div/div/div[1]/a").click()
    driver.get_screenshot_as_file('./kabanLogin.png')
    print('screen')
    driver.implicitly_wait(5)


def kaban_linking():
    print("Find orders.")
    driver.get("https://kabanchik.ua/cabinet/dashboard/p/recommended")
    time.sleep(2)
    driver.implicitly_wait(rand)
    check_kaban_links(driver.page_source)


def check_kaban_links(html_catch):
    global all_data
    kaban_data: list = []
    URL = 'https://kabanchik.ua/cabinet/dashboard/p/recommended'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    links = driver.find_elements(By.CLASS_NAME, "kb-dashboard-performer__title")
    for link in links:
        link_name = link.text
        yes_in = False
        for item in all_data:
            if link_name in item:
                yes_in = True
                break
        if not yes_in:
            time.sleep(1)
            link.click()
            time.sleep(1)
            cur_handlers = driver.window_handles
            driver.implicitly_wait(rand)
            driver.switch_to.window(cur_handlers[1])
            driver.implicitly_wait(2)
            time.sleep(1)
            url = driver.current_url
            kaban_parse(driver.page_source, url)
            time.sleep(rand)
            driver.close()
            driver.implicitly_wait(rand)
            driver.switch_to.window(cur_handlers[0])
            time.sleep(1)


def kaban_parse(html_catch, url):
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

    was_created = soup.find('div', class_='kb-sidebar-grid__content').get_text(strip=True)

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
        message = '\n<b>' + name + '</b>\n<b>'+was_created+'\n' + price + '</b> \n\nDeadline: ' + deadline + \
                  '\n\n<b>ТЗ: </b>\n' + \
                  '' + sTasks + '\n\n<b>Комментарий: </b> ' + comment + '\n\n<b>Клиент: </b> ' + client + ' ' \
                  '\n' + review + ' - ' + positive + \
                  '\n' + 'Url - ' + url
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


def create_code(code):
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = (
        "INSERT INTO `bird_bot`(`code`) VALUES ("+code+")")
    cursor.execute(sql_query)
    cursor.close()


def read_code():
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = (
        "SELECT `code` FROM `bird_bot` WHERE id=1")
    cursor.execute(sql_query)
    code = cursor.fetchall()
    cursor.close()
    print(code)
    return code


def update_code(code):
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = (
        "UPDATE `bird_bot` SET `code`="+code+" WHERE id=1")
    cursor.execute(sql_query)
    code = cursor.fetchall()
    cursor.close()
    return code


def insert_data(coming_data):
    connection = create_connection()
    cursor = connection.cursor()
    sqlData = coming_data
    sql = (
        "INSERT INTO kabanchik2 ( number, name, price, deadline, tasks, comment, client, review, positive )"
        "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, sqlData)
    cursor.close()


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# todo:                                         .. :: Telegram :: ..
def send_telegram(tmessage: str):
    token = "5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4"
    channel_id = "-692711290"
    url2 = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + channel_id + '&parse_mode=' \
                                                                                           'html&text=' + tmessage
    r = requests.post(url2)

    if r.status_code != 200:
        raise Exception("post_text error")


# todo:                                         .. :: Drive Me Baby :: ..


def show_time():
    gmail_login()
    time.sleep(3)

    kaban_login()
    get_data()
    driver.implicitly_wait(3)
    time.sleep(rand)

    i = 1
    while i < 2000:
        time.sleep(1)
        kaban_linking()
        print(i, 'K.A.B.A.N. peris')
        driver.implicitly_wait(3)
        randStart = 110 + rand
        time.sleep(randStart)
        i += 1


# todo:                                         .. :: Telegram Bot :: ..


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} realise the KRAKEN"
    bot.send_message(message.chat.id, msg)
    start_driver()
    time.sleep(3)
    show_time()


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} calm down KRAKEN"
    bot.send_message(message.chat.id, msg)
    stop_driver()


@bot.message_handler(commands=['enter_code'])
def send_welcome(message):
    state['write_sms'] = True
    msg = "..."
    bot.send_message(message.chat.id, msg)


@bot.message_handler()
def send_welcome(message):
    if state['write_sms'] and len(message.text) == 6 and message.text.isdigit():
        msg = "Ok, lets free it..."
        code = message.text
        update_code(code)
        return bot.send_message(message.chat.id, msg)
    if state['write_sms'] and len(message.text) < 6 or state['write_sms'] and len(message.text) > 6:
        msg = "This is piece of shit, not the valid code. Must by 6 symbols"
        return bot.send_message(message.chat.id, msg)
    if state['write_sms'] and len(message.text) == 6 and not message.text.isdigit():
        msg = "Or you have crooked hands. Or you decided to fucking joke. \nIn the code must by no one letters."
        return bot.send_message(message.chat.id, msg)
    else:
        msg = "I don't understand you leather bag."
        bot.send_message(message.chat.id, msg)
    state['write_sms'] = False


bot.infinity_polling()


# Dependencies
# pip3 install -U selenium
# pip3 install webdriver-manager
# pip3 install fake-useragent
# pip3 install pyTelegramBotAPI

# pip freeze - to check all versions
# pip uninstall selenium
# And:
# pip install selenium==3.141.0
