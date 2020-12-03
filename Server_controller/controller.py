# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import socketserver
import serial
import threading

import db_control

HOST = "0.0.0.0"
UDP_PORT = 10000
MICRO_COMMANDS = ["TL", "LT"]
#FILENAME        = "values.txt"
LAST_VALUE = ""


# gestion des messages reçu via UDP
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(
            current_thread.name, self.client_address, data))
        if data != "":
            if data in MICRO_COMMANDS:  # Send message through UART
                sendUARTMessage("00/cmd/" + data)

            elif data == "getValues()":  # Sent last value received from micro-controller
                socket.sendto(LAST_VALUE, self.client_address)

            else:
                print("Unknown message: ", data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


# send serial message
SERIALPORT = "/dev/ttyACM0"
BAUDRATE = 115200
ser = serial.Serial()


def initUART():
    #ser = serial.Serial(SERIALPORT, BAUDRATE)
    ser.port = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = None  # block read

    # ser.timeout = 0             #non-block read
    # ser.timeout = 2              #timeout block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    # ser.writeTimeout = 0     #timeout for write
    print('Starting Up Serial Monitor')
    try:
        ser.open()
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))
        exit()



def sendUARTMessage(msg):
    ser.write(msg)
    print("Message <" + msg + "> sent to micro-controller.")


def ser_listen(message):
    sensorId = message[0]
    messageType = message[1]
    messageContent = message[2]

    if (messageType == "data"):
        dataArray = messageContent.split("&")
        temp =  (dataArray[0]).split(":")[1]
        lum =  (dataArray[1]).split(":")[1]

        tempJson = '{ "value":" '+ temp + '", "type":"T", "sensor":"'+ sensorId +  '"}'
        lumJson  = '{ "value":" '+ lum + '", "type":"L", "sensor":"'+ sensorId +  '"}'

        db_control.Db_Add_data(tempJson)
        db_control.Db_Add_data(lumJson)
        print("adding data : \n" + tempJson + "\n" + lumJson)

    elif (messageType == "error"):
        print(messageContent)
    else :
        print("gateway unknown message : " +  message)




# Main program logic follows:
if __name__ == '__main__':
    initUART()
    print('Press Ctrl-C to quit.')

    server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, UDP_PORT))

        while ser.isOpen():

            if (ser.inWaiting() > 0):  # if incoming bytes are waiting
                data_str = ser.read(ser.inWaiting())
                ser_listen(data_str)
                #print(data_str.decode())
                LAST_VALUE = data_str
                #print(data_str)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        ser.close()
        exit()
