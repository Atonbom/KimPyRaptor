# Discord bot for Arduino UNO

I made a discord bot to control the mBot which I recently named KimPyRaptor which sounds way better. The tutorial (link) posted below describes very elaborated how to make a Discord bot in Python and I really recommend to follow it. In this tutorial you will learn:
- What Discord is
- Why discord.py is so valuable
- How to make a Discord bot in the Developer Portal
- How to create a Discord connection in Python
- How to handle events
- How to create a Bot connection
- How to use bot commands, checks, and converters

https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal 

After you followed this tutorial you are ready to make your own bot and link it to your Arduino in my case the KimPyRaptor. You just have to combine the bot code and the code you made to control your Arduino. On my git I posted the KimPyRaptor bot code have a look if you want to get an idea how to do this. 

If you are using Spyder for your Python you might encounter some errors like: “Cannot close a running event loop”. This is a Spyder related issue and there are several fixes of which a few I will post below. But even with these fixes your code might still not run. My solution is easier, just use another Python IDE. I tried PyCharm for running my bot (after installing all packages ofcourse) and it works without any problems.
 
Spyder (optional) Fixes/Threads for “Cannot close a running event loop” ERROR

- https://docs.aiohttp.org/en/stable/ 
- https://pypi.org/project/nest-asyncio/
- https://stackoverflow.com/questions/57639751/how-to-fix-runtime-error-cannot-close-a-running-event-loop-python-discord-bot 
- https://stackoverflow.com/questions/64297553/python-discord-bot-code-returns-runtimeerror-cannot-close-a-running-event-lo 
- https://stackoverflow.com/questions/50243393/runtimeerror-this-event-loop-is-already-running-debugging-aiohttp-asyncio-a 
- https://stackoverflow.com/questions/51862318/python-asyncio-runtimeerror-cannot-close-a-running-event-loop 
- https://stackoverflow.com/questions/61308995/cannot-close-a-running-event-loop-discord-bot-creation 
- https://www.xspdf.com/resolution/55409641.html 
