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
status = "TL"

initialize(pinReset=pin0)
clear_oled()
# Les deux fonctions suivantes permettent de récupérer
# les valeurs de la température et de la luminosité.
# Elles sont isolées car utilisées à plusieurs endroits du code.
def recupval_t():
    Temp = temperature()
    text_Temp = "Temp = " + str(Temp)
    return text_Temp
def recupval_L():
    Lum = display.read_light_level()
    text_Lum = "Lum = " + str(Lum)
    return text_Lum

def radio_contact(): #Fonction d'envoi de données et réception de réponses

        radio.send(PIN)
        todo = radio.receive()
        if todo.split("/")[1] == "cmd":
            if status == "TL":
                status = "LT"
            else:
                status = "TL"
        elif todo.split("/")[1] == "ask":
            data_t = recupval_t()
            data_L = recupval_L()
            radio.send("01/data/T:"+ data_t + "&" + "L:" + data_L)

            while radio.receive() != "ACK":
                sleep(10)

        else:
            radio.send("00/error/umr")

while True:
    txt_Temp = recupval_t()
    txt_Lum = recupval_L()

    if (button_a.is_pressed()) or (button_b.is_pressed()):
        clear_oled()

        if (status == "TL"):
            add_text(0, L1, txt_Temp)
            add_text(0, L2, txt_Lum)
            status = "LT"
        else :
            add_text(0, L2, txt_Temp)
            add_text(0, L1, txt_Lum)
            status = "TL"