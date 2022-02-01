# pip install mysql-connector-python
# -*- coding: utf-8 -*-
import json

from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error


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


# .................................................................:: Parse MinFin ::...................................


def parse_MinFin():
    URL = 'https://index.minfin.com.ua/markets/fuel/tm/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find('table', class_='zebra')
    result = result.findAll('tr')
    return result


# .................................................................:: Parse KLO ::...................................


def parse_KLO():
    URL = 'https://index.minfin.com.ua/markets/fuel/tm/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find('table', class_='zebra')
    result = result.findAll('tr')
    return result


# .................................................................:: Fill MinFin ::....................................


def fill_MinFin(selector):
    result: list = []
    for item in items:
        try:
            item.find('a').get_text(strip=True).find('+')
        except:
            send_telegram(
                "<b>[ where ]: </b> today-taxi\n"
                + "<b>[ section ]: </b> parsing fuel\n"
                + "<b>[ error ]: </b> item.find('a').get_text(strip=True).find('+')"
            )

        if item.find('a').get_text(strip=True).find('+') < 0:
            prices = item.findAll('td', class_=selector)

            count: int = 0
            array: list = []
            titles = ["title", "br", "95+", "95", "92", "df", "gas"]
            for price in prices:
                title = titles[count]
                count = count + 1
                if title == "title":
                    array.append({
                        title: price.find('a').get_text(strip=True).replace('\xad', '').replace('\xa0', ' ')
                    })
                if title != "title":
                    array[0][title] = price.get_text(strip=True)
            if len(array) > 0:
                result.append(array[0])

    return json.dumps(result)


# .................................................................:: INSERT INTO DB ::.................................


items = parse_MinFin()
items2 = fill_MinFin('r1')
items3 = fill_MinFin('r0')
item_res = items2 + items3


# .................................................................:: Create Connection ::..............................


def create_connection(host_name, user_name, user_password, db_name):
    connect = None
    try:
        connect = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        send_telegram(
            "<b>[ where ]: </b> today-taxi\n"
            + "<b>[ section ]: </b> parsing fuel\n"
            + "<b>[ error ]: </b> ошибка связи с БД. >INSERT<"
        )
        print(f"The error '{e}' occurred")

    cursor = connect.cursor()

    add_parse = "UPDATE fuel SET json = ( %s) WHERE id = 1"
    data_parse = [str(item_res)]
    print(data_parse)
    try:
        cursor.execute(add_parse, data_parse)
    except:
        send_telegram(
            "<b>[ where ]: </b> today-taxi\n"
            + "<b>[ section ]: </b> parsing fuel\n"
            + "<b>[ error ]: </b> cursor.execute(add_parse, data_parse)"
        )
    return connect


if len(item_res) > 0:
    connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
else:
    send_telegram(
        "<b>[ where ]: </b> today-taxi\n"
        + "<b>[ section ]: </b> parsing fuel\n"
        + "<b>[ error ]: </b> вероятно, искомые элементы небыли найдены. Массив данных пуст!"
    )
