from microbit import *
import radio

SENSOR_PIN = 1245

uart.init(baudrate=115200, bits=8, parity=None, stop=1)
display.scroll('Uart ready')

radio.on()
radio.config(channel=1)        # Choose your own channel number
radio.config(power=7)


def uart_handle(): 

    msg_bytes = uart.read()

    messageArray = message.split("/")
    messageType = messageArray[1]
    messageContent = messageArray[2]

    if messageType == "cmd":
        radio.send("00/cmd/" + messageContent)
        
    else:
        Uart_send("error : unknown command")



def Radio_handle():
    message = radio.recieve()
    messageArray = message.split("/")

    messageType = messageArray[1]
    messageContent = messageArray[2]

    if messageType == "ask" :
        if (messageContent == SENSOR_PIN) :
            # print("PIN correct") #TODO Communication serveur pour obtenir un id
            radio.send("00/ans/01")
        else :
            # print("incorrect PIN")
            radio.send("00/ans/99")

    elif messageType == "data" :
        Uart_send(message)

    else :
        Uart_send("00/error/sensor unknown message")
    


def Uart_send(msg):
    print(msg)


def Radio_send(msg):
    radio.send(msg)


while True:

    if (button_a.get_presses()):
        Uart_send('Bonjour')

    if (button_b.get_presses()):
        Radio_send('Bonjour')

    if (radio.recieve() != None ):
        Radio_handle()

    if uart.any():
        uart_handle()


    sleep(10)  # sleep 10 ms
    
    
    
    
    
    
    
    
    
    
    
    
    
