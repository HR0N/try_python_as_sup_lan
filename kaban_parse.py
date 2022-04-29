# pip install mysql-connector-python
# pip install mysql-connector-python

from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome("chromedriver.exe")
import requests
import mysql.connector
from mysql.connector import Error

def kaban_login():
    link = "https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser"
    session = requests.Session()
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    data = {
        "name": "identifier",
    }
    # response = session.post(link, data=data, headers=HEADERS).text


kaban_login()

def kaban_suka_parse():
    URL = 'https://kabanchik.ua/cabinet/dashboard/p/recommended'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

# kaban_suka_parse()

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
    data = 0
    data_parse = [str(data)]
    # add_parse = ("INSERT INTO weather ( json ) VALUES ( %s)")
    add_parse = ("UPDATE weather SET json = ( %s) WHERE id = 1")
    # cursor.execute(add_parse, data_parse)
    # "UPDATE weather ( json ) VALUES ( %s)"

    return connection

# connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
# examplepass123