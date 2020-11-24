''''
microbit.uart.init(baudrate=9600, bits=8, parity=None, *, stop=1,  tx=pin219, rx=pin20)
sleep(2000)
uart.write('hello world') #Envoie des lignes au serveur apres 2 sec
uart.write(b'hello world')


while True:

    if(uart.any()): #Si un message UART du serveur il recoit
        msg_bytes = uart.read()
        msg_str = str(msg, 'UTF-8')
        display.scroll(msg_str)


