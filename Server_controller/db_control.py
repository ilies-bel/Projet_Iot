import sqlite3
import json
from datetime import datetime

DB_PATH = 'db/server_data.db'


def Db_connect():
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return connection


def Db_close():
    sqlite3.connect(DB_PATH).close()


def Db_Add_data(data):  # Permet d'ajouter une ligne a la BDD a partir d'un objet JSON
    dbRow = []
    try:
        parsedData = json.loads(data)

        # conversion temperature en Kelvin pour ajout en base
        value = float(parsedData["Value"])
        dataType = parsedData["Type"]
        if (dataType == "T"):
            value = value + 273.15

        dbRow.append(value)
        dbRow.append(dataType)
        dbRow.append(datetime.now())
        dbRow.append(parsedData["User"])

        connection = Db_connect()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO data ( Value,Type,Date,UserId) VALUES (?,?,?,?)', dbRow)
        connection.commit()
    except :
        print("The message is not in JSON format : ", data)


def Db_displayData():
    connection = Db_connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM data')
    print(cursor.fetchall())


# ----------------------------Testing Zone
''''
# JSON data test
x = '{ "Value":"12", "Type":"T", "User":"1"}'

Db_Add_data(x)

Db_displayData()


Db_close()
# print(datetime.now())
'''''