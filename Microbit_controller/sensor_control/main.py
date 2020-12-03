from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio

PIN = "1245"
L1 = 0
L2 = 2
SENSOR_ID = "01"
STATUS = "TL"

initialize(pinReset=pin0)
clear_oled()

def oled_init():
    add_text(0, L1, "initializing")
    add_text(0, L2, "data")

def radioSendData():
    temp = str(temperature())
    lum = str(display.read_light_level())
    msg = SENSOR_ID + "/data/T:"+ temp + "&L:" + lum
    radio.send(msg)



def radio_contact(message): #Fonction d'envoi de données et réception de réponses
        messageArray = message.split("/")
        if messageArray[1] == "cmd":
            status = messageArray[2]
            if (status == "TL"):
                STATUS = "LT"
            else :
                STATUS = "TL"
            temp = str(temperature())
            lum = str(display.read_light_level())
            txt_Temp = "Temp = " + temp
            txt_Lum =  "Lum = " + lum
            if (STATUS == "TL"):
                clear_oled()
                add_text(0, L1, txt_Temp)
                add_text(0, L2, txt_Lum)
            else:
                clear_oled()
                add_text(0, L2, txt_Temp)
                add_text(0, L1, txt_Lum)

        elif messageArray[1] == "ans":
            SENSOR_ID = messageArray[2]

        else:
            radio.send("00/error/umr")


oled_init()
radio.on()
radio.config(channel=1)
radio.config(power=7)
radio.send(SENSOR_ID + "/ask/"+ PIN)

while True:
        message = radio.receive()
        if message != None:
           radio_contact(message)
        radioSendData()
        sleep(0.1) # sleep de 100 ms