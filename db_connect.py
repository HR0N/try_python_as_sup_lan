# pip install mysql-connector-python

import json
from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error

items2 = ''
def parse():
    URL = 'https://index.minfin.com.ua/markets/fuel/tm/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('table', class_='zebra')
    items = items.findAll('tr')
    items2 = str(items)
    items2 = json.dumps(items2)
    print(items2)
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

    cursor = connection.cursor()

    add_parse = ("INSERT INTO fuels ( parse ) VALUES ( %s)")
    print(type(items2))
    data_parse = ['items2']
    # cursor.execute(add_parse, data_parse)

    return connection



connection = create_connection("pr435071.mysql.tools", "pr435071_fuelparse", "82aA!m9J#u", "pr435071_fuelparse")