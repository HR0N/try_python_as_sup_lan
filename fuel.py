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


# .................................................................:: Parse Data::...................................


def parse_univ(url, elem1, elem2, elem1_class='', elem2_class=''):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find(elem1, class_=elem1_class)
    result = result.findAll(elem2, class_=elem2_class)
    return result


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
    URL = 'https://www.klo.ua/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find('section', class_='general-price')
    result = result.findAll('div', class_='general-price-item')
    return result


# .................................................................:: Fill MinFin ::....................................


def fill_MinFin(selector):
    result: list = []
    for item in min_fin:
        try:
            item.find('a').get_text(strip=True).find('+')
        except:
            send_telegram(
                "<b>[ where ]: </b> today-taxi\n"
                + "<b>[ section ]: </b> parsing fuel - Fill MinFin\n"
                + "<b>[ error ]: </b> <code>item.find('a').get_text(strip=True).find('+')</code>"
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
                        title: price.find('a').get_text(strip=True).replace('\xad', '').replace('\xa0', '')
                    })
                if title != "title":
                    array[0][title] = price.get_text(strip=True)
            if len(array) > 0 and array[0]['title'] != "KLO":
                result.append(array[0])
            if len(array) > 0 and array[0]['title'] == "KLO":
                result.append(fill_KLO()[0])

    return result

# .................................................................:: Fill KLO ::....................................


def fill_KLO():
    array: list = []
    # titles = ["title", "br", "95+", "95", "92", "df", "gas"]
    for item in klo:
        print('item', item)
        try:
            item.find('div', class_='general-price-item__title').get_text(strip=True)
        except:
            send_telegram(
                "<b>[ where ]: </b> today-taxi\n"
                + "<b>[ section ]: </b> parsing fuel - Fill KLO\n"
                + "<b>[ error ]: </b> <code>item.find('a').get_text(strip=True).find('+')</code>"
            )
        title = item.find('div', class_='general-price-item__title').get_text(strip=True)
        price = item.find('div', class_='general-price-item__value').get_text(strip=True).replace(' грн', '')
        if title == "F 100":
            array.append({"title": "KLO", "br": ""})
        if title == "Euro 95":
            array[0]["95+"] = price
        if title == "95 Shebel":
            array[0]["95"] = price
        if title == "92 Shebel":
            array[0]["92"] = price
        if title == "Diesel Euro":
            array[0]["df"] = price
        if title == "Газ":
            array[0]["gas"] = price
    return array


# .................................................................:: INSERT INTO DB ::.................................


# min_fin = parse_MinFin()
# klo = parse_KLO()
# parse_univ(url, elem1, elem2, elem1_class, elem2_class)
min_fin = parse_univ('https://index.minfin.com.ua/markets/fuel/tm/', 'table', 'tr', 'zebra')
klo = parse_univ('https://www.klo.ua/', 'section', 'div', 'general-price', 'general-price-item')
min_fin2 = fill_MinFin('r1')
min_fin3 = fill_MinFin('r0')
min_fin4 = json.dumps(min_fin2 + min_fin3)
item_res = min_fin4


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
            + "<b>[ section ]: </b> parsing fuel - Create Connection\n"
            + "<b>[ error ]: </b> ошибка связи с БД. >INSERT<"
        )
        print(f"The error '{e}' occurred")

    cursor = connect.cursor()

    add_parse = "UPDATE fuel SET json = ( %s) WHERE id = 1"
    # add_parse = ("INSERT INTO fuel ( json ) VALUES ( %s)")
    data_parse = [str(item_res)]
    try:
        print(data_parse)
        cursor.execute(add_parse, data_parse)
    except:
        send_telegram(
            "<b>[ where ]: </b> today-taxi\n"
            + "<b>[ section ]: </b> parsing fuel - Create Connection\n"
            + "<b>[ error ]: </b> <code>cursor.execute(add_parse, data_parse)</code>"
        )
    return connect


if len(item_res) > 0:
    connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
else:
    send_telegram(
        "<b>[ where ]: </b> today-taxi\n"
        + "<b>[ section ]: </b> parsing fuel - Create Connection\n"
        + "<b>[ error ]: </b> вероятно, искомые элементы небыли найдены. Массив данных пуст!"
    )
