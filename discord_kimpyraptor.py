# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:07:48 2021

@author: Atonbom
https://github.com/atonbom 
https://forum.makeblock.com/u/Atonbom/activity
"""
#Discord bot for KimPyRaptor
#Run this script using Pycharm if Spyder gives errors like: "cannot close a running event loop"
#This is a Spyder related issue


import discord
from discord.ext import commands


#for driving
import serial
import time


bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")



# Events
@bot.event
async def on_ready():
    #Look intoooooo thissssss
    await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="http://www.twitch.tv/accountname"))
    print('KimPyRaptor ready for Duty')

@bot.command(name='start', help='Wake Up KimPyRaptor')
async def start_bot(ctx):
    # Define the serial port and baud rate.
    # Default baud rate for mBot USB is 9600 and 115200 for Bluetooth
    # Ensure the 'COM#' is correctly selected for the mBot
    global ser
    ser = serial.Serial('COM10', 9600)
    time.sleep(2)  # wait for the serial connection to initialize
    response = "KimPyRaptor is Fired Up and ready to Go!!!"
    await ctx.send(response)
    
@bot.command(name='w', help='Drive KimPyRaptor forward')
async def drive_forward(ctx):
    time.sleep(0.1) 
    ser.write('w'.encode('utf-8'))
    response = "Driving Forward"
    await ctx.send(response)

@bot.command(name='s', help='Drive KimPyRaptor backwards')
async def drive_backward(ctx):
    time.sleep(0.1)
    ser.write('s'.encode('utf-8'))
    response = "Driving Backward"
    await ctx.send(response)

@bot.command(name='a', help='Turn KimPyRaptor left ')
async def turn_left(ctx):
    time.sleep(0.1)
    ser.write('a'.encode('utf-8'))
    response = "Turning left"
    await ctx.send(response)

@bot.command(name='d', help='Turn KimPyRaptor right')
async def turn_right(ctx):
    time.sleep(0.1)
    ser.write('d'.encode('utf-8'))
    response = "Turning right"
    await ctx.send(response)


@bot.command(name='sleep', help='Send KimPyRaptor to bed')
async def stop_bot(ctx):
    time.sleep(0.1)
    ser.write('q'.encode('utf-8'))
    ser.close()
    response = "KimPyRaptor is dreaming of Chinks"
    await ctx.send(response)

bot.run('ODA1Nzk3NTQwNTI3NDcyNjUw.YBgHcA.Ti12ST6Rtmr5LABRQ45iH_FBxXI')