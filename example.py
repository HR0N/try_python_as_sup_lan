import time
from functools import wraps
import mysql.connector
from mysql.connector import Error
import re
import telebot
bot = telebot.TeleBot("5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4", parse_mode='html')


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


def retry(times):
    def wrapper_fn(f):
        @wraps(f)
        def new_wrapper(*args,**kwargs):
            for i in range(times):
                try:
                    print('try %s' % (i + 1))
                    return f(*args,**kwargs)
                except Exception as e:
                    time.sleep(1)
                    error = e
            raise error
        return new_wrapper
    return wrapper_fn


@retry(5)
def send_message():
    return 1/0


print(send_message())

