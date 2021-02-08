# NodeMCU V3 ESP8266 serial WiFi bridge for Arduino UNO / mBot


To wirelessly communicate with the mBot it’s possible to connect an ESP8266 to the mBot. Why would you want this? 

- The mBot itself doesn’t have a WiFi module to communicate wirelessly  
- The standard Bluetooth module often doesn’t work without the Makeblock Bluetooth dongle
- You can remotely control you mBot by reading/writing serial data over WiFi

The main set-up looks like this:

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
