# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:19:06 2021

@author: Atonbom
https://github.com/atonbom 
https://forum.makeblock.com/u/Atonbom/activity
"""

# Drive_mBot_Keyboard
# Python script for driving the mBot with keyboard using a serial connection
# Corresponding arduino script => mBot_drive_serialV2.ino

import serial
import time

# Define the serial port and baud rate.
# Default baud rate for mBot USB is 9600 and 115200 for Bluetooth
# Ensure the 'COM#' is correctly selected for the mBot
ser = serial.Serial('COM10', 9600)

time.sleep(2) # wait for the serial connection to initialize


#Drive function
#Input for direction: w/a/s/d
#Speed is standard set to 100 in .ino file
#L/R turns standard only drive 1 wheel other wheel keeps still
def drivepy_keyboard():
    
    global user_input
    
    user_input = input("\n Type w / a / s / d / quit: ")
    if user_input =="w":
        print("Driving Forward")
        time.sleep(0.1) 
        ser.write('w'.encode('utf-8')) 
    elif user_input =="a":
        print("Turn Left")
        time.sleep(0.1)
        ser.write(b'a')
    elif user_input =="s":
        print("Drive Backwards")
        time.sleep(0.1)
        ser.write(b's')
    elif user_input =="d":
        print("Turn Right")
        time.sleep(0.1)
        ser.write(b'd')
    elif user_input =="quit" or user_input == "q":
        print("Program Exiting")
        time.sleep(0.1)
        ser.write(b'q')
        ser.close()
    else:
        print("Invalid input. Type on / off / quit.")


#========================
# The actual loop / program
        
while True:
    drivepy_keyboard()
    if user_input == "q" or user_input == "quit":
        break