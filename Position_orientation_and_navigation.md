# Position, orientation and navigation of the robot
Python is a very powerful programming language, relatively “easy” and also supports serial communication. Therefore it’s an excellent choice for this project to control the robot. Now that it’s possible to send commands via serial communication and control the robot it’s time to implement a system to determine the position and orientation of the robot in order to navigate it to a specified destination. A top view camera is used to do this.



## Position and orientation
The images of the camera in this project are pulled using the OpenCV library for Python. This library provides hundreds of real-time optimized computer vision algorithms and is very user-friendly. 
Before determining the orientation of the robot it first has to be localized. This was done by placing two squares in different colors on top of the robot. The script than makes masks for each color and draws contours around the objects. After that it searches for the 2 largest enclosing rectangles and calculates the center coordinates (centroids) on the frame.


## This section is not yet finished
