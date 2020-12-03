from microbit import *
import radio

uart.init(baudrate=115200, bits=8, parity=None, stop=1)
display.scroll('Uart ready')

radio.on()
radio.config(channel=1)        # Choose your own channel number
radio.config(power=7)
display.scroll('Radio ch 1')
radio_waiting = False



def listen():
    if uart.any():
        msg_bytes = uart.read()
        display.scroll(msg_bytes)
        """if msg_bytes==b'temperature':
            temp=temperature()
            print(temp)
            display.scroll(temp)
        elif msg_bytes==b'coucou':
            display.scroll('coucou')"""
    if radio_waiting:
        display.scroll('Att')


def radio_listen():
    message = radio.recieve()
    messageType = message[1]
    messageContent = message[2]

def Uart_send(msg):
    print(msg)


def Radio_send(msg):
    display.scroll('Radio : ' + msg)
    radio.send(msg)


while True:

    if (button_a.get_presses()):
        Uart_send('Bonjour')

    if (button_b.get_presses()):
        Radio_send('Bonjour')
    if (radio.recieve() != None ):
        radio_listen()
    listen()
    sleep(10)  # sleep 10 ms
    
    
    
    
    
    
    
    
    
    
    
    
    
