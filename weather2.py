# pip install mysql-connector-python
# pip install mysql-connector-python
import datetime
from threading import Timer

from bs4 import BeautifulSoup
import requests
import mysql.connector
import random

now = datetime.datetime.now()

array: list = []


# .................................................................:: Telegram ::....................................


def send_telegram(text: str):
    token = "5274529590:AAGSDTirzUQAgIH2Sp-SdkS3tqlXsHeGKqA"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001755786077"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text,
        "parse_mode": 'HTML'
    })

    if r.status_code != 200:
        raise Exception("post_text error")


def get_days():
    URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/10-%D0%B4%D0%BD%D0%B5%D0%B9'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', {"class": "main"})
    result: list = []
    for item in items:
        result.append(int(item.find('p', {'class', 'date'}).get_text(strip=True)))
    return result


def get_data(url):
    # URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/10-%D0%B4%D0%BD%D0%B5%D0%B9'
    URL = url
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', {"id": "blockDays"})
    item_tab = items.find('div', {"class", "tabsContentInner"}).findAll('table', {'class', 'weatherDetails'})
    return item_tab


def store_data(data):
    array.append(data)


def fill_data(url):
    print(get_data(url))


fill_data('https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/2022-02-18')


def call_sinoptik():
    days = get_days()
    date = ''
    # get_data('https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/2022-02-18')
    i = 0

    print(days)
    for day in days:
        url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/'
        month = now.month
        year = now.year
        nDay = days[i]
        if i + 1 < len(days) and days[i] > days[i + 1]:
            month = month + 1
        if month == 13:
            month = 1
            year = year + 1
        if int(month) < 10:
            month = '0' + str(month)
        if int(nDay) < 10:
            nDay = '0' + str(nDay)
        date = str(year) + '-' + str(month) + '-' + str(nDay)
        url = url + date
        rand = random.randint(1, 3)
        Timer(((i * 3) + rand), fill_data, [url]).start()
        i = i + 1


# Timer(1, call_sinoptik).start()
# call_sinoptik()


def create_connection(host_name, user_name, user_password, db_name):
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
        send_telegram(
            "<b>[ where ]: </b> today-taxi\n"
            + "<b>[ section ]: </b> parsing weather 2 - create connection\n"
        )

    cursor = connection.cursor()

    data_parse = [str(data)]
    # add_parse = ("INSERT INTO weather ( json ) VALUES ( %s)")
    add_parse = ("UPDATE weather2 SET json = ( %s) WHERE id = 1")
    # cursor.execute(add_parse, data_parse)
    # "UPDATE weather ( json ) VALUES ( %s)"

    return connection

# connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
