import sqlite3
import random
import json
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from datetime import datetime


DB_HOST = 'localhost'
DB_PORT = '8086'


def Db_connect():

    try:
        client = InfluxDBClient(host=DB_HOST, port=DB_PORT)
    except:
        print("Unable to connect to database")
    return client


def Db_Add_data(data):  # Permet d'ajouter une ligne a la BDD a partir d'un objet JSON

    print(data)
    
    try:

        client = Db_connect()
        client.switch_database('data')
        parsedData = json.loads(data)

        now = str(datetime.now())
        value = parsedData["value"]
        
        
        if (parsedData["type"] == "T"):
            dataType = "temperature"

        if (parsedData["type"] == "L"):
            dataType = "luminosite"

        json_body = [
            {
                "measurement": dataType,
                "tags": {
                    "sensor": parsedData["sensor"],
                },
                "time": now,
                "fields": {
                    "value": value
                }
            }
        ]

        print(json_body)
        
        client.write_points(json_body, database='data', time_precision='ms')

    except (InfluxDBClientError, InfluxDBServerError) as e:
        print("unable to write on database : ", e)

# ----------------------------Testing Zone 

# JSON data test
"""
for k in range(1000):
    rand = random.randint(120,300)/10
    x = '{ "value":"' + str(rand) + '", "type":"T", "sensor":"1"}'
    Db_Add_data(x)
"""
