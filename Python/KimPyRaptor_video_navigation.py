# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:09:46 2021

@author: Atonbom
https://github.com/atonbom 
https://forum.makeblock.com/u/Atonbom/activity
"""


# import the necessary packages
import numpy as np
import imutils
import cv2
import serial
import time
from math import atan2, degrees

# Define the serial port and baud rate.
# Default baud rate for mBot USB is 9600 and 115200 for Bluetooth
# Ensure the 'COM#' is correctly selected for the mBot
ser = serial.Serial('COM10', 9600)
time.sleep(2) # wait for the serial connection to initialize


# define the lower and upper boundaries of the "green and pink object"
# in the HSV color space, then initialize the
# list of tracked points
# Front
colorLower1 = (89, 100, 100)
colorUpper1 = (109, 255, 255)
#Back
colorLower2 = (60, 100, 100)
colorUpper2 = (80, 255, 255)



#define the camera
camera = cv2.VideoCapture(0)

#Initializing variables
targetx = None
targety = None
bx = None
by = None
fx = None
fy = None
cx = None
cy = None
center1 = None
center2 = None
center3 = None

#Time for sleeping, this influences how often commands are being send to the robot
#If the bot is overloaded with commands or gets to twitchy you can increase the sleep time 
sleeptime = 0


while True:
    ########### Localization of the bot ###########
    ###############################################

    # grab the current frame
    (grabbed, frame) = camera.read()

    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Mask1
    # construct a mask for the color of the front, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask1 = cv2.inRange(hsv, colorLower1, colorUpper1)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)

    #Mask2
    # construct a mask for the color of the back, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask2 = cv2.inRange(hsv, colorLower2, colorUpper2)
    mask2 = cv2.erode(mask2, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)    

    # find contours in the mask1 and initialize the current
    # (x, y) center of the object
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    
    # find contours in the mask2 and initialize the current
    # (x, y) center of the object
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    

    # only proceed if at least one contour was found
    if len(cnts1) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing rectangle
        cnt1 = max(cnts1, key=cv2.contourArea)
        rect1 = cv2.minAreaRect(cnt1)
        box1 = cv2.boxPoints(rect1)
        box1 = np.int0(box1)
        
        #centroid computation of front
        M1 = cv2.moments(cnt1)
        center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
        fx,fy =center1
        
        #draw contour2 and center2 on the frame
        cv2.drawContours(frame, [box1], 0, (0, 0, 255), 2)
        cv2.circle(frame, center1, 3, (0, 0, 255), -1)
    else:
        center1 = None

        
    # only proceed if at least one contour was found
    if len(cnts2) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing rectangle
        cnt2 = max(cnts2, key=cv2.contourArea)
        rect2 = cv2.minAreaRect(cnt2)
        box2 = cv2.boxPoints(rect2)
        box2 = np.int0(box2)
        
        #centroid computation of back
        M2 = cv2.moments(cnt2)
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        bx,by =center2
        
        #draw contour2 and center2 on the frame
        cv2.drawContours(frame, [box2], 0, (100, 255, 255), 2)
        cv2.circle(frame, center2, 3, (255, 255, 100), -1)
    else:
        center2 = None
        


    ########### Orientation of the bot  ###########
    ###############################################
    if center1 != None and center2 != None:    
        #Q1 0-90 degrees
        if bx<fx and by>fy:
            zb=by-fy
            zf=fx-bx
            orientation = int(degrees(atan2(zf,zb)))
            #calculate centroid coordinates of bot
            print('q1')
            cx = int(0.5*zf+bx)
            cy = int(0.5*zb+fy)
            center3 = cx,cy
        #Q2 90-180 degrees
        elif bx<fx and by<fy:
            zb=fx-bx
            zf=fy-by
            orientation = int(degrees(atan2(zf,zb))+90)  
            #calculate centroid coordinates of bot
            print('q2')
            cx = int(0.5*zb+bx)
            cy = int(0.5*zf+by)
            center3 = cx,cy
        #Q3 180-270 degrees
        elif bx>fx and by<fy:
            zb=fy-by
            zf=bx-fx
            orientation = int(degrees(atan2(zf,zb))+180)
            #calculate centroid coordinates of bot
            print('q3')
            cx = int(0.5*zf+fx)
            cy = int(0.5*zb+by)
            center3 = cx,cy
        #Q4 270-360 degrees
        elif bx>fx and by>fy:
            zb=bx-fx
            zf=by-fy
            orientation = int(degrees(atan2(zf,zb))+270)
            #calculate centroid coordinates of bot
            print('q4')
            cx = int(0.5*zb+fx)
            cy = int(0.5*zf+fy)
            center3 = cx,cy   
        cv2.circle(frame, center3, 3, (255, 0, 0), -1)
    else: center3 = None                         
                              
   
    ###########    Setting a Target     ###########
    ############################################### 
    
    def target(event,x,y,flags,param):  
        global targetx,targety
        # checking for left mouse clicks 
        if event == cv2.EVENT_LBUTTONDOWN:
            targetx,targety=x,y
               
    cv2.setMouseCallback('Frame', target)
    
    #check if a target is present and draw a circle
    if targetx != None:
        print("x ", targetx, " y ", targety)
        cv2.circle(frame,(targetx,targety), 5, (0, 255, 0), -1)
        

    ###########  Angle target and bot   ###########
    ###############################################                
    #check if a target is set and a bot  is present
    if targetx != None and center3 != None:
        
        #Stop the bot when it reaches the target within a set range of pixels
        stoprange = 20
        if abs(cx-targetx) <= stoprange and abs(cy-targety) <= stoprange:
            time.sleep(sleeptime)
            ser.write('q'.encode('utf-8'))
            print("Goal reached waiting for commands")
        
        else:
            # Calculate the angle of the target relatively
            # to the center of the bot. (Top of screen is 0 degrees)
            #Q1 0-90 degrees
            if cx<targetx and cy>targety:
                zc=cy-targety
                zt=targetx-cx
                targetangle = int(degrees(atan2(zt,zc)))
            #Q2 90-180 degrees
            elif cx<targetx and cy<targety:
                zc=targetx-cx
                zt=targety-cy
                targetangle = int(degrees(atan2(zt,zc))+90)  
            #Q3 180-270 degrees
            elif cx>targetx and cy<targety:
                zc=targety-cy
                zt=cx-targetx
                targetangle = int(degrees(atan2(zt,zc))+180)
            #Q4 270-360 degrees
            elif cx>targetx and cy>targety:
                zc=cx-targetx
                zt=cy-targety
                targetangle = int(degrees(atan2(zt,zc))+270)
         
            
    ###########       Navigation        ###########
    ###############################################   
    # Calculate the angle between the orientation of the bot and the target
    # If angle is within the set interval
    # bot drives forward otherwise it will turn
    
            #Navigation interval +/-
            #delta is in degrees
            delta = 20
            if targetangle-delta >= 0 and targetangle+delta <= 360:
                interval = [targetangle-delta, targetangle+delta]
            elif targetangle-delta <= 0:
                interval = [360+targetangle-delta, targetangle+delta]
            elif targetangle+delta >= 360:
                interval = [targetangle-delta, targetangle+delta-360] 
            print ("interval ", interval)
        
            # Move commands      
            # Forward
            if orientation >= interval[0] and orientation <= interval[1]:
                print("Driving Forward")
                time.sleep(sleeptime) 
                ser.write('w'.encode('utf-8')) 
            
            else:
                # Calculate the "angle" to make when turning left or right
                leftangle = orientation-interval[1]
                rightangle = interval[0]-orientation
                # Correct for negative angle
                if leftangle <= 0:
                    leftangle += 360
                if rightangle <= 0:
                    rightangle += 360
                    
                # Determine which direction to turn to
                # Forward, this is needed when heading towards top of screen
                if leftangle >= 180 and rightangle >= 180:
                   print("Driving Forward")
                   time.sleep(sleeptime) 
                   ser.write('w'.encode('utf-8')) 
                # Turn Left
                elif leftangle <= rightangle:
                    print("Turning Left")
                    time.sleep(sleeptime) 
                    ser.write('a'.encode('utf-8')) 
                    
                # Turn Right    
                elif rightangle <= leftangle:
                    print("Turning Right")
                    time.sleep(sleeptime) 
                    ser.write('d'.encode('utf-8')) 
                # print ("left angle ",leftangle)
                # print ("right angle ",rightangle)
                # print ("orientation ", orientation)
                
    else:
        print("No Bot detected or target set")
        time.sleep(sleeptime) 
        ser.write('q'.encode('utf-8'))
                     
        
    # show the frame and mask to our screen
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask1', mask1)
    cv2.imshow('Mask2', mask2)
    key = cv2.waitKey(1) & 0xFF
  
    
  
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
ser.write('q'.encode('utf-8')) 
ser.close()