import mysql.connector
from mysql.connector import Error
import re


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


def insert_data2(coming_data):
    connection = create_connection()
    cursor = connection.cursor()
    sqlData = str(coming_data)
    print(type(sqlData))
    print(sqlData)
    sql = (
        f"INSERT INTO `kabanchik3`(`order_id`) VALUES ('{sqlData}')")
    cursor.execute(sql, sqlData)
    cursor.close()


list2 = []
list3 = {'test': 'test2'}
price = 'test'
price2 = 'test2'
list2.append(price)
list2.append(price2)

testStr = 'что за ххуйня 🥶'
testStr = re.sub('[^\x00-\x7Fа-яА-Я]', '', testStr)

insert_data2(testStr)

