import sqlite3
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
    payload = []

    try:

        client = Db_connect()
        client.switch_database('data')
        parsedData = json.loads(data)

        now = str(datetime.now())
        # conversion temperature en Kelvin pour ajout en base
        value = parsedData["value"]
        
        
        if (parsedData["type"] == "T"):
            dataType = "temperature"
            
            #value = value + 273.15
        
        '''
        dbRow = {
            'measurement': value,
            'tags': {},
            'type': dataType,
            'time': now,
            'userId': parsedData["sensor"],
        }
        '''
        # payload.append(dbRow)
        

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
        # payload.append(data)
        
        #client.write_points(json_body, )
        client.write_points(json_body, database='data', time_precision='ms')

    except (InfluxDBClientError, InfluxDBServerError) as e:
        print("unable to write on database : ", e)


''''
def Db_displayData():

    client = Db_connect()
    cursor.execute('SELECT * FROM data')
    print(cursor.fetchall())
'''''


# ----------------------------Testing Zone
''''
# JSON data test
x = '{ "Value":"12", "Type":"T", "User":"1"}'

Db_Add_data(x)

Db_displayData()


Db_close()
# print(datetime.now())
'''''
# JSON data test
x = '{ "value":"15", "type":"T", "sensor":"1"}'


#Db_Add_data(x)

'''
client.switch_database('data')
results = client.query('SELECT * FROM temperature')
points = results.get_points()

print(points)
'''


# print(client.get_list_database())
# client.switch_database("data")

# points = results.get_points(tags={'userId': '1'})
# for point in points:
# print("Time: %s, Duration: %i" % (point['time'], point['duration']))
