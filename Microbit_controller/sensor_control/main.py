from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio
import string
PIN = 1245
radio.config(channel=1)
radio.config(power=7)
L1 = 0
L2 = 2
SENSOR_ID = 99
STATUS = "TL"

initialize(pinReset=pin0)
clear_oled()
# Les deux fonctions suivantes permettent de récupérer
# les valeurs de la température et de la luminosité.
# Elles sont isolées car utilisées à plusieurs endroits du code.


def radio_init():
    radio.send(PIN)

def oled_init():
    add_text(0, L1, "initialising")
    add_text(0, L2, "data")

def get_temp():
    Temp = temperature()
    text_Temp =str(Temp)
    return text_Temp
def get_lum():
    Lum = display.read_light_level()
    text_Lum = str(Lum)
    return text_Lum    

def oled_set(status):
    if (status == "TL"):
        add_text(0, L1, txt_Temp)
        add_text(0, L2, txt_Lum)
        STATUS = "LT"
    else :
        add_text(0, L2, txt_Temp)
        add_text(0, L1, txt_Lum)
        STATUS = "TL"

def oled_write(temp, lum)

    tempString = "Temp = " + temp
    lumString =  "Lum = " + lum
    add_text(0, L1, tempString)
    add_text(0, L2, lumString)

def radio_send_data():
    temp = get_temp()
    lum = get_lum()
    oled_write(tempString,lumString)
    radio.send( SENSOR_ID + "/data/T:"+ temp + "&L:" + lum)



def radio_contact(): #Fonction d'envoi de données et réception de réponses
        message = radio.receive()
        messageArray = message.split("/")
        if messageArray[1] == "cmd":
            oled_set(messageArray[2])

        elif messageArray[1] == "ans":
            SESOR_ID = messageArray[2]

        else:
            radio.send("00/error/umr")



oled_init()
radio_init()

while True:


    if (button_a.is_pressed()) or (button_b.is_pressed()):
        clear_oled()

