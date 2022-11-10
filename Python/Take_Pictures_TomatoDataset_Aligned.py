# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:20:16 2021

@author: Atonbom
https://github.com/Atonbom/KimPyRaptor 
https://forum.makeblock.com/u/Atonbom/activity
"""

#This code is used to take pictures of tomatoes/objects an build a dataset
#It captures an rgb image and a depth image and aligns these two
#An annotation file is created after taking the pictures which can be used in the deeplearning model to estimate tomato weight


#This code will take color and depth pictures by using a Intel Realsense camera
#The code works with a D435
#Also the depth map of the pictures is saved in a csv file
#When running the code a picture can be taken by pressing the "space bar"
#Before running the code please define the angle, batch, distances, repetition, species, age
#and location of the "weight.csv" file
#This information will be used for the filenames and making an annotation .csv file
#Press "Esc" to exit the script
#When "repeat" is higher than 1 and you have more than 1 distance the script assumes that you
#first take all the pictures for the 1st distance than the 2nd distance etc..
#At the end of the code a "weight_volume.csv" file will be combined with the other annotation data
#into a new annotation .csv file.

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import Pandas for handling dataframes
import pandas as pd

#Initialize dataframe to save annotation data
annotation = pd.DataFrame(columns=
['file_id', #unique id for the file
'species', #species of tomato
'age', # in days (approximately)
'weight', # real weight in grams
'volume', # real volume in ml
'density', # density of the tomato in g/cm3 or g/ml
'distance', # distance is the real measured distance of tomato to camera in cm
'angle', # angle of the camera relative to the surface
'batch', # batch number inside the dataset
'truss_id', #truss id inside the batch
'object_id', # object id inside the batch
'unique_batch_id', # unique id for every datapoint/photo inside the batch
'healthy']) # is the tomato healthy yes or no, this is not measured or calculated but rather an observation

###############################################################################

#Insert here the angle of the camera towards the surface
#For instance "45d" for a 45 degrees angle or "09d" for a 9 degrees angle
angle ='20d'

#Insert here the batch number in 2 digits i.e. "06" or "15"
#Maximum is "99"
batch = '08'

#Insert here the distances to the camera in cm where you will put the object, use 3 digits
#distance = ['030','050','070','090','110']
#distance = ['040','060']
distance = ['030','035','040','050','060']

#Insert here how many pictures/photos per object per distance should be taken
#Maximum is 9
repeat = 1

#Insert here the species of the tomatoes/objects
species = 'Merlice'

#Insert here the age of the tomatoes/objects approximately in days
age = '48'

#Define location of "weight_volume.csv" file should contain 7 columns
#first column should contain "object_id"
#second column should contain the "truss_id"
#third column should contain the weight in grams 
#sixth column the volume in ml
#seventh column the density in g/cm3 or g/ml
#4th and 5th column can be used as calculation columns or left empty
weight_volume_dataframe = pd.read_csv('output_pics/weight_volume.csv', sep=';', header=0)
weight_volume = weight_volume_dataframe.values

###############################################################################

#####################################################
##              Align Depth to Color               ##
##            And Initialize the stream            ##
#####################################################

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
# different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)



#Initializing a count variable to give every file an id
i = 0

#Initialize object_id
object_id = 0

#Initializing a count variable for "object_id"
#the same "object_id" can be used for multiple files if "repeat" is higher than 1
j = 1

#Initializing a count variable for the distances
k = 0

# Streaming loop
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Render depth image to depth color image:
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    
        #Show the color and depth images on screen
        cv2.imshow("depth color image", depth_colormap)
        cv2.imshow("Color image", color_image)
        
        #If statement, when spacebar pressed take picture and determine the filename
        #Based on repeat, angle, batch, object_id, distance and unique batch id
        key = cv2.waitKey(1)
        if key == 32:
            if i<10:
                ii = "00"+str(i)
            elif i<100:
                ii = "0"+str(i)
            else:
                ii = str(i)
            i+=1
            
            if k > len(distance)-1:
                object_id+=1
                k = 0
            distance_str = distance[k]
            
            iteration=j
            if j >= repeat:
                k+=1
                j = 1
            else:
                j += 1
                
            if object_id<10:
                object_id_str = "00"+str(object_id)
            elif object_id<100:
                object_id_str = "0"+str(object_id)
            else:
                object_id_str=str(object_id)
            
            #Write pictures to a tiff file
            file_id = str(repeat)+"x"+angle+batch+object_id_str+distance_str+ii
            cv2.imwrite("output_pics/color{0}.tiff".format(file_id),color_image)
            cv2.imwrite("output_pics/depth{0}.tiff".format(file_id),depth_colormap)
            
            #write depth dataframe to .csv file
            depth = depth_image            
            df = pd.DataFrame(depth)
            df.to_csv("output_pics/depthdata{0}.csv".format(file_id))
            
            #write information to annotation .csv file
            annotation = annotation.append({'file_id': file_id,
                                            'species': species,
                                            'age': age,
                                            'weight': weight_volume[int(object_id_str)][2],
                                            'volume': weight_volume[int(object_id_str)][5],
                                            'density': weight_volume[int(object_id_str)][2]/weight_volume[int(object_id_str)][5],
                                            'distance': distance_str,
                                            'angle': angle,
                                            'batch': batch,
                                            'truss_id': weight_volume[int(object_id_str)][1],
                                            'object_id': object_id_str,
                                            'unique_batch_id': ii},
                                            ignore_index=True)
            
            #print statements for checking
            print('Repeat:',str(repeat)+"x")
            print('Angle:',angle)
            print('Batch:',batch)
            print('Object id:',object_id_str)
            print('Distance:',distance_str)
            print('Unique batch id:',ii)
            print('Iteration:',iteration)
            print('Saved Frame')
            print('')
            
            #Make an info screen to show information about previous picture taken
            #make a black image to print text on
            img = np.zeros((800, 1500))
            cv2.putText(img,'Object id:'+object_id_str,(20,100),cv2.FONT_HERSHEY_COMPLEX,3.5,(255,255,255),thickness = 3)
            cv2.putText(img,'Distance:'+distance_str,(20,300),cv2.FONT_HERSHEY_COMPLEX,3.5,(255,255,255),thickness = 3)
            cv2.putText(img,'Unique batch id:'+ii,(20,500),cv2.FONT_HERSHEY_COMPLEX,3.5,(255,255,255),thickness = 3)
            cv2.putText(img,'Iteration:'+str(iteration),(20,700),cv2.FONT_HERSHEY_COMPLEX,3.5,(255,255,255),thickness = 3)
            cv2.imshow("A box!", img)
            
            
        if key == 27:
            annotation.to_csv("output_pics/annotation{0}.csv".format(str(repeat)+"x"+angle+batch))
            print ("Exit")
            break

finally:
    pipeline.stop()
  