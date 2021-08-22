# temp file - only includes serial communication with arduino

import serial
from time import sleep 

arduino1Serial = serial.Serial('COM10', baudrate = 9600, timeout = 1)


def arduinoCommunication():

    if infoReceived == 'g': # dispensing
        arduino1Serial.write(b'g')

    elif infoReceived == '1': # dispensing
        arduino1Serial.write(b'1')
    
    elif infoReceived == '2': # dispensing
        arduino1Serial.write(b'2')

    elif infoReceived == '3': # dispensing
        arduino1Serial.write(b'3')
    
    elif infoReceived == '4': # dispensing
        arduino1Serial.write(b'4')
    
    elif infoReceived == '0': # dispensing
        arduino1Serial.write(b'0')



while True: 
    infoReceived = input(": ")
    arduinoCommunication()

