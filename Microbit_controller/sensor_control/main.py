from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *

L1 = 0
L2 = 2
status = "TL"

initialize(pinReset=pin0)
clear_oled()


while True:
    Temp = temperature()
    textTemp = "Temp = " + str(Temp)
    Lum = display.read_light_level()
    textLum = "Lum = " + str(Lum)

    if (button_a.is_pressed()) or (button_b.is_pressed()):
        clear_oled()

        if (status == "TL"):
            add_text(0, L1, textTemp)
            add_text(0, L2, textLum)
            status = "LT"
        else :
            add_text(0, L2, textTemp)
            add_text(0, L1, textLum)
            status = "TL"