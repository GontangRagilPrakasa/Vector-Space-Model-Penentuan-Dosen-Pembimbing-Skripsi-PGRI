import mysql.connector
from mysql.connector import Error
import time
import datetime
import csv
import itertools

def connection():
    return mysql.connector.connect(host='localhost',
                                         port = 3306,
                                         database='vsm_teacher',
                                         user="root",
                                         password="")

#https://www.freecodecamp.org/news/connect-python-with-sql/
def read_all(query):
    connection = mysql.connector.connect(host='localhost',
                                         port = 3306,
                                         database='vsm_teacher',
                                         user="root",
                                         password="")
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def read_with_params(query, params):
    connection = mysql.connector.connect(host='localhost',
                                         port = 3306,
                                         database='vsm_teacher',
                                         user="root",
                                         password="")
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query,params)
        result = cursor.fetchone()
        return result
    except Error as err:
        print(f"Error: '{err}'")