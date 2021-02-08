As I said before it’s also possible to program the mCore directly using Arduino code written in the Arduino IDE.
When writing more advanced programs and when you for instance want to control your bot using a python script it’s better to use this instead of mBot.

If you are not familiar with writing C++ code (Arduino is also C++) I recommend taking the time to do some tutorials
or if you’re confident enough take a look at some example sketches from the makeblock library. 

But what is a library? Look here for the formal definition: https://www.arduino.cc/en/main/libraries.
Makeblock also has its own library with a lot of predefined functions for things like controlling the motors. Instead of defining pin’s and setting timers etc. 
you just include the library for your bot and call on the functions.

Makeblock library: https://github.com/Makeblock-official/Makeblock-Libraries 

I recommend taking a good look at their github and follow the instructions, take the time to understand it.

Besides the pros of using libraries there are also some cons some of which you will probably encounter along the way.
One of the most annoying but expected one was the following:
I tried to use the integrated buzzer on the board but instead of using MeBuzzer I used pin 8 (to which the buzzer is connected) and called on the tone() function.
For the motors I did use the library and this is what caused conflict. The tone function apparently uses the same timer as the IR sensor in the library.
So when I compiled the code I got the following error: *Tone.cpp.o (symbol from plugin): In function `timer0_pin_port': (.text+0x0): multiple definition of `__vector_13'*

Now you might think IR sensor? Yes the mCore also has an integrated IR sensor and receiver. And even though in my code I was not using this sensor I still got the error. 
This is due to the fact that I included the MeMcore.h library.
So when compiling the code everything is checked and compiled even the functions you don’t use.
C++ is very strict in this sense and unforgiving opposite to Python where you can easily define things 3 times different in a row and make very messy code.
Which often works but if it doesn’t and your code is quite extended then well good luck…
Moral of this story C++ is strict which prevents errors but also can be annoying because you have to write workarounds or rewrite libraries.
The last I certainly wouldn’t recommend because if a library will be updated in the future you would have to rewrite again and who knows probably a new problem arises.
