from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *

PASSWORD = "IOT_Password28" # TODO stockage + sécurisé ?

Temp = "Temperature 12.5 C"
Lum = "Luminosité 65"

L1 = 0
L2 = 2
status = "TL"

initialize(pinReset=pin0)
clear_oled()


while 1:

    if (button_a.is_pressed()) or (button_b.is_pressed()): #pour testing
        clear_oled()
        if (status == "TL"):
            add_text(0, L1, Temp)
            add_text(0, L2, Lum)
            status = "LT"
        else :
            add_text(0, L2, Temp)
            add_text(0, L1, Lum)
            status = "TL"

        



