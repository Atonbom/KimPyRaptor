# Serial Communication

Writing a program for your robot which it executes when you start it up is nice of course 
but if you want to control your robot by commands given from a device you need something extra. 
The easiest way to do this is using serial communication.
By default the mBot has 1 serial port with 2 “connectors”. The first one is the USB-B port and the second one is where the Bluetooth module is connected. 
What must be NOTED is that it’s only possible to communicate with 1 of them and not both at the same time.

Formal definition of serial on Arduino: https://www.arduino.cc/reference/en/language/functions/communication/serial/

This is an easy tutorial on what serial communication is and how you can use with your Arduino:
https://www.norwegiancreations.com/2017/12/arduino-tutorial-serial-inputs/#:~:text=Using%20serial%20inputs%20is%20not,on%20your%20keyboard%20to%20send 

Above tutorial gives you a working example and how to use it but lacks some explanation about certain parameters and code but it’s fairly simply really.

The code below show how you start up / initialize the serial connection and you only have to execute it once so that’s why it is in the setup(). 
The number 9600 is the baud rate and defines the rate at which information is transferred in a communication channel. 
Here is some more detailed information regarding baud rate and the Arduino: https://www.quora.com/What-is-the-baud-rate-and-why-does-Arduino-have-a-baud-rate-of-9-600. 

But the thing to remember is: Default baud rate of an Arduino UNO is 9600. 
And if you want to set-up a serial connection you must make sure that on both sides the baud rate is the same e.g. robot 9600 and Arduino serial monitor 9600.

![](https://github.com/Atonbom/KimPyRaptor/blob/main/Images/serial1.png)

In the tutorial two ways of reading serial data are proposed: Serial.read() and Serial.readStringUntil(). 
Both work and especially the Serial.readStringUntil() seems like a very nice function to read commands consisting of multiple characters. 
BUT if you search the internet for this function you will see a lot of hate and it is advised to stay far away from this function. 
Look it up if you are interested. Luckily there are other ways to read multiple characters, I won’t go into details but will post a tutorial which also addresses this. 

![]https://github.com/Atonbom/KimPyRaptor/blob/main/Images/serial2.png

![]https://github.com/Atonbom/KimPyRaptor/blob/main/Images/serial3.png

One question you should always ask yourself when using serial commands is: “Do my commands need to consist of multiple characters?”. 
For instance if you want to send a command for “Drive Forward” you could sent this entire command or simply sent “w” for instance. 
You may think computers are fast and in Python for instance this wouldn’t matter much (up until a certain point ofcourse) but due to the characteristics of serial communication it does matter.
So try to keep your code and commands as minimalistic as possible to gain high speeds. 
Of course if you don’t care about latency do whatever you want, btw you should always do whatever you want.

To give an example of the impact of using readStringUntil() compared to read(): I wrote a python script that sent serial command to my mBot.
When I used readStringUntil() it took my bot 2 sec to respond and start driving even though I was sending a single character. 
Then I tried read() and the bot responded in an instant. So if you want to do real time monitoring or control I advise to use Serial.read(). 

Serial inputs basics tutorial:
https://forum.arduino.cc/index.php?topic=396450.0 
