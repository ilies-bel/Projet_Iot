from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *

while true:

    if (button_a.is_pressed()) or (button_b.is_pressed()):
        initialize(pinReset=pin0)
        clear_oled()
        add_text(0, 0, "Salut !!!")

# initialize(pinReset=pin0)
# clear_oled()
# add_text(0, 0, "Salut !!!")
