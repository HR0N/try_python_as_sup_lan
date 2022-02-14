# pip install mysql-connector-python
# pip install mysql-connector-python

from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error


def get_data():
    URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', {"id": "mainContentBlock"})

    print(items)

    return items


get_data()

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

    data_parse = [str(data)]
    # add_parse = ("INSERT INTO weather ( json ) VALUES ( %s)")
    add_parse = ("UPDATE weather2 SET json = ( %s) WHERE id = 1")
    # cursor.execute(add_parse, data_parse)
    # "UPDATE weather ( json ) VALUES ( %s)"

    return connection

connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
