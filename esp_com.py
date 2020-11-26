# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 21:08:04 2018

@author: User
"""

import serial
 
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM6'
ser.open()
 
values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
ser.write(values)
 
total = 0
 
while total < len(values):
    print(ord(ser.read(1)))
    total=total+1
 
ser.close()