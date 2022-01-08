# pip install mysql-connector-python
# pip install mysql-connector-python

from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error

arr3 = []
arr10 = []


def removeDegree(str1):
    return str1.replace('°', '')


def formulaFtoC(f):  # Formula °F to °C: (1 °F − 32) × 5/9
    return (f - 32) * 5 / 9


def tenDays():
    URL = 'https://weather.com/weather/tenday/l/d198c31dca17aa9ac8e4ff2e4dbdb48e4ca8c01f0fd1369998f0a09f53ef0b1d#detailIndex5'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', class_='DailyForecast--DisclosureList--msYIJ')
    items = items.findAll('details', class_='Disclosure--themeList--25Q0H')

    for item in items:  # Formula °F to °C: (1 °F − 32) × 5/9 = -17,22 °C
        title = item.find('span', class_='DailyContent--daypartDate--2A3Wi').get_text(strip=True)
        highTempValue = item.find('span', class_='DetailsSummary--highTempValue--3Oteu').get_text(strip=True)
        lowTempValue = item.find('span', class_='DetailsSummary--lowTempValue--3H-7I').get_text(strip=True)
        rain = item.find('span', class_='DailyContent--value--37sk2').get_text(strip=True)
        wind = item.find('span', class_='Wind--windWrapper--3aqXJ DailyContent--value--37sk2').get_text(strip=True)
        DetailsTable = item.findAll('span', class_='DetailsTable--value--1q_qD')
        humidity = DetailsTable[0].get_text(strip=True)
        UVIndex = DetailsTable[1].get_text(strip=True)
        if highTempValue != '--':
            highTempValue = int(removeDegree(highTempValue))
            highTempValue = round(formulaFtoC(highTempValue))
        if lowTempValue != '--':
            lowTempValue = int(removeDegree(lowTempValue))
            lowTempValue = round(formulaFtoC(lowTempValue))
        wind = wind.replace(' mph', '')
        wind = round(int("".join(c for c in wind if c.isdecimal())) * 1.60934)          # mp/h * 1.60934 = km/h


        arr10.append({
            'title': title,
            'highTempValue': highTempValue,
            'lowTempValue': lowTempValue,
            'rain': rain,
            'wind': wind,
            'humidity': humidity,
            'UVIndex': UVIndex,
        })
    return items


tenDays()
def threeDays():
    URL = 'https://weather.com/weather/hourbyhour/l/d198c31dca17aa9ac8e4ff2e4dbdb48e4ca8c01f0fd1369998f0a09f53ef0b1d'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('div', class_='HourlyForecast--DisclosureList--3CdxR')
    items = items.findAll('details', class_='Disclosure--themeList--25Q0H')

    for item in items:  # Formula °F to °C: (1 °F − 32) × 5/9 = -17,22 °C
        title = item.find('h2', class_='DetailsSummary--daypartName--2FBp2').get_text(strip=True)
        temperatureValue = item.find('span', class_='DetailsSummary--tempValue--1K4ka').get_text(strip=True)
        rain = item.find('div', class_='DetailsSummary--precip--1ecIJ').find('span').get_text(strip=True)
        DetailsTable = item.findAll('li', class_='DetailsTable--listItem--2yVyz')
        feelsLike = DetailsTable[0].find('span', class_='DetailsTable--value--1q_qD').get_text(strip=True)
        wind = item.find('span', class_='Wind--windWrapper--3aqXJ DetailsTable--value--1q_qD').get_text(strip=True)
        humidity = DetailsTable[2].find('span', class_='DetailsTable--value--1q_qD').get_text(strip=True)
        UVIndex = DetailsTable[3].find('span', class_='DetailsTable--value--1q_qD').get_text(strip=True)
        cloudCover = DetailsTable[4].find('span', class_='DetailsTable--value--1q_qD').get_text(strip=True)
        precipAmount = DetailsTable[5].find('span', class_='DetailsTable--value--1q_qD').get_text(strip=True)


        temperatureValue = int(removeDegree(temperatureValue))
        temperatureValue = int(formulaFtoC(temperatureValue))
        feelsLike = int(removeDegree(feelsLike))
        feelsLike = round(formulaFtoC(feelsLike))
        wind = wind.replace(' mph', '')
        wind = round(int("".join(c for c in wind if c.isdecimal())) * 1.60934)  # mp/h * 1.60934 = km/h
        precipAmount = round(float(precipAmount.replace(' in', '')) * 2.54, 1)
        if precipAmount == 0.0: precipAmount = 0
        precipAmount = str(precipAmount) + ' cm'

        arr3.append({
            'title': title,
            'temperatureValue': temperatureValue,
            'rain': rain,
            'feelsLike': feelsLike,
            'wind': wind,
            'humidity': humidity,
            'UVIndex': UVIndex,
            'cloudCover': cloudCover,
            'precipAmount': precipAmount,

        })
    return items


threeDays()

data = [arr3, arr10]


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
    add_parse = ("UPDATE weather SET json = ( %s) WHERE id = 1")
    cursor.execute(add_parse, data_parse)
    # "UPDATE weather ( json ) VALUES ( %s)"

    return connection

connection = create_connection("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api")
