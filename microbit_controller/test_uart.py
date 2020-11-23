from microbit import *

microbit.uart.init(baudrate=9600, bits=8, parity=None, stop=1, *, tx=None, rx=None)
sleep(2000)
uart.write('hello world') #Envoie des lignes au serveur après 2 sec
uart.write(b'hello world')


while True:

    if(uart.any()): #Si un message UART du serveur il reçoit
        msg_bytes = uart.read()
        msg_str = str(msg, 'UTF-8')
        display.scroll(msg_str)


