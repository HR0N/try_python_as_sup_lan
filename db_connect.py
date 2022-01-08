# pip install mysql-connector-python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error


def parse():
    URL = 'https://index.minfin.com.ua/markets/fuel/tm/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('table', class_='zebra')
    items = items.findAll('tr')
    return items
parse()


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

    items3 = arr_sprint([], 'r1')
    items4 = arr_sprint(items3, 'r0')

    cursor = connection.cursor()

    add_parse = ("INSERT INTO fuel ( json ) VALUES ( %s)")
    data_parse = [str(items4)]
    print((data_parse))
    cursor.execute(add_parse, data_parse)

    return connection

def arr_sprint(arr, selector):
    items2 = parse()

    items3 = arr
    for item in items2:
        if(item.find('a').get_text(strip=True).find('+') < 0):
            prices = item.findAll('td', class_=selector)

            count: int = 0
            arr: list = []
            titles = ["title", "br", "95+", "95", "92", "df", "gas"]
            for price in prices:
                title = titles[count]
                count = count + 1
                if(title == "title"):
                    arr.append({
                        title: price.find('a').get_text(strip=True).replace('\xad', '').replace('\xa0', ' ')
                    })
                if (title != "title"):
                    arr[0][title] = price.get_text(strip=True)
            items3.append(arr)

    return items3




#connection = create_connection("pr435071.mysql.tools", "pr435071_fuelparse", "82aA!m9J#u", "pr435071_fuelparse")
connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
