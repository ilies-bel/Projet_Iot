from microbit import *
import radio

SENSOR_PIN = "1245"

uart.init(baudrate=115200, bits=8, parity=None, stop=1)

radio.on()
radio.config(channel=1)  # Choose your own channel number
radio.config(power=7)


def uart_handle():
    msg_bytes = (uart.read())
    msg_str = str(msg_bytes, 'UTF-8')
    
    messageArray = msg_str.split("/")
    messageType = messageArray[1]
    messageContent = messageArray[2]

    if messageType == "cmd":
        display.scroll("send cmd")
        radio.send(msg_bytes)

    else:
        Uart_send("00/err/unknown command")


def radio_handle(message):
    messageArray = message.split("/")
    sensorId = messageArray[0]
    messageType = messageArray[1]
    messageContent = messageArray[2]

    if messageType == "ask":
        if (messageContent == SENSOR_PIN):
            radio.send("00/ans/01")
        else:
            radio.send("00/ans/99")

    elif messageType == "data" and sensorId != "99":
        Uart_send(message)

    else:
        Uart_send("00/error/sensor unknown message")


def Uart_send(msg):
    print(msg)


while True:

    if (button_a.is_pressed()):
        print('00/data/T:25&L:255')
        display.scroll('uart send')



    if (button_b.is_pressed()):
        print('00/cmd/LT')

    message = radio.receive()

    if (message != None):
        radio_handle(message)

    if uart.any():
        uart_handle()

    sleep(0.1)  # sleep 100 ms
