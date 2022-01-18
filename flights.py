# pip install mysql-connector-python
# pip install mysql-connector-python

from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
import datetime

x = datetime.datetime.now()
x = (str(x).split('.')[1])

l = len(x)

Remove_last = x[:l-2]


arr3 = []
arr10 = []



def getFlights():
    URL = 'https://kbp.aero/wp-content/themes/borispol-magenta/js/board.js?v=1642517448' + '.' + Remove_last
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    # items = soup.find('div', class_='DailyForecast--DisclosureList--msYIJ')
    # items = items.findAll('details', class_='Disclosure--themeList--25Q0H')
    sSoup = str(soup)
    sSoup = sSoup.split(' = ')
    sSoup = sSoup[1]
    sSoup = sSoup.replace('\n', '')
    sSoup = sSoup.replace('\t', '')
    sSoup = sSoup.replace(';', '')

    return sSoup


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

    data = getFlights()

    data_parse = [str(data)]
    # add_parse = ("INSERT INTO flights ( json ) VALUES ( %s)")
    add_parse = ("UPDATE flights SET json = ( %s) WHERE id = 1")
    # print(data_parse)
    cursor.execute(add_parse, data_parse)
    # "UPDATE flights ( json ) VALUES ( %s)"

    return connection

connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
