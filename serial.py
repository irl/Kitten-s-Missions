#!/usr/bin/env python2

import serial
TTY = '/dev/ttyACM0'
ser_port = serial.Serial(TTY, 9600, rtscts = 1)
print ser_port.portstr

def readInput():
    if(ser_port.inWaiting()):
        return ser_port.read()
