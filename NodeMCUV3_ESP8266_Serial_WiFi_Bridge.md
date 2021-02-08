# NodeMCU V3 ESP8266 serial WiFi bridge for Arduino UNO / mBot


To wirelessly communicate with the mBot it’s possible to connect an ESP8266 to the mBot. Why would you want this? 

- The mBot itself doesn’t have a WiFi module to communicate wirelessly  
- The standard Bluetooth module often doesn’t work without the Makeblock Bluetooth dongle
- You can remotely control you mBot by reading/writing serial data over WiFi

The main set-up looks like this:
![Flowchart esp8266 mbot](https://github.com/Atonbom/KimPyRaptor/blob/main/Images/Flowchart_esp_mbot_jpg.jpg)

For this project I used a NodeMCU ESP8266 v3. It’s possible to connect the ESP8266 to the RX/TX pins of the board or to use one of the “white” RJ25 sensors ports of the mBot.
The difference is that RJ25 ports communicate via I2C instead of UART. Both have their advantages and disadvantages, take a look at this link if you are interested: https://www.seeedstudio.com/blog/2019/09/25/uart-vs-i2c-vs-spi-communication-protocols-and-uses/ 

I will explain how to set-up both methods

## UART
Using this method the ESP8266 will be connected to the RT/TX pins of the board. I used the following materials make it function properly. It is of course possible to use different components but this will probably require some other electrical components to make it function properly from an electrical engineering point of view.
-	NodeMCU V3 ESP8266
-	Diode 1N4148
-	Resistor 1k2
-	Wire 0.25mm2 (preferably 4 colors)

I used the following tutorial to setup the system, I suggest to take a look before continuing with my specific example. https://www.youtube.com/watch?v=mtazgora9xE&t=665s 

The steps to follow are:
1.	Flash the ESP8266 with ESP-Link https://github.com/jeelabs/esp-link  Watch the YouTube video and/or follow the git
2.	Before you can start wiring the ESP8266 to the mBot you may have to disconnect/remove the Bluetooth module if not done already. This is because you will be using the pins from this module to connect your ESP8266 to.
3.	Wire the ESP8266 to your mBot.  This is the most important part because it differs per ESP8266 if and how you place resistors diodes etc. Instead of wiring the TX to RX and RX to TX I wired TX D7 (GPIO13) and RX D8 (GPIO15) on the ESP8266. The reason is that on boot the ESP8266 outputs some random garbage which will go into your mBot. This can cause issues like for instant your robot starts to drive and won’t respond to your commands anymore. By using D7, D8 and a pulldown resistor this can be overcome according to jeelabs. https://github.com/jeelabs/esp-link/blob/master/FLASHING.md 
TX D7 also have a diode. D7 is always high so when TX is low it pulls D7 low. This is different than seen in the YouTube video and many other diagrams you might find on the internet. This is mainly because most ESP’s work on 3.3v and in order to power it via the Arduino which is 5V you need a voltage divider. But the NodeMCU V3 can be powered using 5V so there is no need for such a divider. In the Photos folder you can find more pictures of the “real life” setup.
![wiring esp8266 mbot](https://github.com/Atonbom/KimPyRaptor/blob/main/Images/ESP8266_mBot_circuitDiagram.jpg)
<img src="https://github.com/Atonbom/KimPyRaptor/blob/main/Images/20210204_130358.jpg" width="386.4" height="515.2"> |
<img src="https://github.com/Atonbom/KimPyRaptor/blob/main/Images/20210204_130358.jpg" width="386.4" height="515.2">


https://github.com/Atonbom/KimPyRaptor/blob/main/Images/20210204_130358.jpg
4.	Configure and test if you can access ESP-link using the Web Server. Watch the YouTube video and/or follow the git. 
5.	After you did this go to the home tab and from pin assignment presets select “esp-12 swap” and click on change. It should look like this:
6.	Go to Debug log tab and turn the UART debug log: off. This is very important and took me a long time to figure out. If you keep it turned on every now and then the ESP8266 will transmit some data which your Arduino will receive data which your Arduino will receive and executes. In my case my robot started to randomly drive around. I found out by hooking the ESP8266 up to all possible wires in the circuit to figure out where the signal came from. When I found it and couldn’t think my way out of it I tried re-flashing the ESP8266 and also tried 3 other ESP’s. Because at some point the night before around 01:45 it worked perfectly. And of course working when tired and not documenting everything will land you in a situation like this. But 18 hours later and one fried ESP8266 I figured it out again and it had nothing to do with the hardware but with a stupid setting…. A lesson to never forget.
7.	The next step is setting up a virtual com port on your pc. There are several tools to do this I recommend: HW Virtual Serial Port. The YouTube Video explains how to set it up. NOTE: use port 2323 for serial commands. It should also be possible to upload sketches over WiFi but so far I haven’t succeeded at this, but normal serial communication works great.
8.	And now test your connection using a serial monitor and have fun!

After you setup everything the next time you only have to do the following things:
1.	Turn on the mBot
2.	Open the virtual COM port on your pc
3.	Run your python script or whatever you are using to communicate

## I2C
Here will be a tutorial about connecting an ESP8266 through I2C with the mBot
