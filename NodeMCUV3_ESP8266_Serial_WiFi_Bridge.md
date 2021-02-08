# NodeMCU V3 ESP8266 serial WiFi bridge for Arduino UNO / mBot


To wirelessly communicate with the mBot it’s possible to connect an ESP8266 to the mBot. Why would you want this? 

- The mBot itself doesn’t have a WiFi module to communicate wirelessly  
- The standard Bluetooth module often doesn’t work without the Makeblock Bluetooth dongle
- You can remotely control you mBot by reading/writing serial data over WiFi

The main set-up looks like this:

For this project I used a NodeMCU ESP8266 v3. It’s possible to connect the ESP8266 to the RX/TX pins of the board or to use one of the “white” RJ25 sensors ports of the mBot.
The difference is that RJ25 ports communicate via I2C instead of UART. Both have their advantages and disadvantages, take a look at this link if you are interested: https://www.seeedstudio.com/blog/2019/09/25/uart-vs-i2c-vs-spi-communication-protocols-and-uses/ 

I will explain how to set-up both methods

##UART
Using this method the ESP8266 will be connected to the RT/TX pins of the board. I used the following materials make it function properly. It is of course possible to use different components but this will probably require some other electrical components to make it function properly from an electrical engineering point of view.
-	NodeMCU V3 ESP8266
-	Diode 1N4148
-	Resistor 1k2
-	Wire 0.25mm2 (preferably 4 colors)

I used the following tutorial to setup the system, I suggest to take a look before continuing with my specific example. https://www.youtube.com/watch?v=mtazgora9xE&t=665s 

