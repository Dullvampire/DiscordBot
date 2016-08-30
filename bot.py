'''
Discord Bot

To invite to server
https://discordapp.com/oauth2/authorize?client_id=212451598352384002&scope=bot&permissions=12659727
'''

#UTF-8 Encoding

import discord
import asyncio
from time import time, sleep
import sys
import os
import datetime

from math import *
import numpy as np

import _thread as thread

from matplotlib import pyplot as plt
from matplotlib import pylab as pyl
import random

import configparser
from flask.helpers import send_file

sleep(0.5)

EPOCH = datetime.datetime.utcfromtimestamp(0)
CLIENT_ID = '212451598352384002'
TOKEN = 'MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk'
COMMAND_START = '*'

config = configparser.ConfigParser()

config.read('settings.ini')

DEFAULT = config['DEFAULT']
NAMES = config['NAMES']

client = discord.Client()

NAME = 'Rivenbot'

COMMAND_LIST = ['*help', '*restart', '*exit', '*update']
COMMANDS = {'*help' : 'Gives this!',
            '*restart' : 'Restarts ' + NAME,
            '*exit' : 'Quits ' + NAME,
            '*update' : 'Pulls update from github'}

@client.async_event
def on_ready ():
    
    for server in client.servers:
        if str(server.id) in NAMES:
            yield from client.change_nickname(server.me, NAMES[str(server.id)])
        else:
            yield from client.change_nickname(server.me, NAME)
    
    if len(client.servers) == 0:
        pass
    elif len(client.servers) == 1:
        print('Connected to ' + str(len(client.servers)) + " server!")
    else:
        print('Connected to ' + str(len(client.servers)) + " servers!")
    
    if DEFAULT['restart'] == 'false':
        for server in client.servers:
            yield from sendMessage(server.default_channel, "I'm here :heart:")
    
    else:
        ownersSentTo = []
        
        for server in client.servers:
            if server.owner not in ownersSentTo:
                yield from sendMessage(server.owner, "I was sucessfully restarted! I go to live another day")
                ownersSentTo.append(server.owner)
                
        DEFAULT['restart'] = 'false'
        
        save()

@client.async_event
def on_server_join (server):
    print('Joined ' + server.name)
    for channel in server.channels:
        try:
            yield from sendMessage(channel, "Hello there, I am " + NAME + " :heart:")
        except discord.errors.HTTPException:
            pass

@client.async_event
def on_member_join (member):
    yield from sendMessage(member.server.default_channel, "Hi " + member.display_name + " :heart:")

@client.async_event
def on_member_remove (member):
    yield from sendMessage(member.server.default_channel, "Oh... Was it my fault " + member.display_name + "? :broken_heart:")

@client.async_event
def on_member_update (before, after):
    if after != after.server.me:
        if before.game == after.game and before.roles == after.roles and before.status == after.status:
            server = after.server
            yield from sendMessage(server.default_channel, "Hey " + before.display_name + " did you change something? You look different...")
            asyncio.sleep(10)
            yield from client.send_typing(server.default_channel)
            asyncio.sleep(3)
            changed = ''
            
            if before.display_name != after.display_name:
                changed = 'name, I like it a lot'
            
            elif before.avatar != after.avatar:
                changed = 'profile pick, looking fine as usual ' + after.display_name
                
            print(before.display_name, after.display_name)
            
            yield from sendMessage(server.default_channel, "You did O.o your " + changed + '!')
    
@client.async_event
def on_message (message):
    content = message.content
    
    try:
        do = message.server.me != message.author
    except:
        do = True
        
    if do:
        if content.startswith(COMMAND_START + 'help'):
            s = ''
            
            for i in COMMAND_LIST:
                s += i + " - " + COMMANDS[i] + '\n'
            
            yield from sendMessage(message.channel, s)
        
        if content.startswith(COMMAND_START + 'set') and message.author == message.server.owner:
            try:
                args = content.split(' ')
                
                if args[1] not in config or args[2] not in config[args[1]]:
                    raise IndexError
                
                config[args[1]][args[2]] = args[3]
                save()
            
            except:
                yield from sendMessage(message.channel, "Sorry, %s doesnt appear to be a setting" % (args[1] + ' - ' + args[2]))
        
        if content.startswith(COMMAND_START + 'restart'):
            for server in client.servers:
                for channel in server.channels:
                    try:
                        yield from sendMessage(channel, "Restarting really quick, BRB")
                    except discord.errors.HTTPException:
                        pass
            
            DEFAULT['restart'] = 'true'
            
            save()
            thread.start_new_thread(os.system, ('run.bat',))
            exit()
        
        if content.startswith(COMMAND_START + 'update'):
            for server in client.servers:
                for channel in server.channels:
                    try:
                        yield from sendMessage(channel, "Updating really quick, BRB")
                    except discord.errors.HTTPException:
                        pass
            save()
            os.system('update.bat')
            thread.start_new_thread(os.system, ('run.bat',))
            exit()
        
        if content.startswith(COMMAND_START + 'exit'):
            for server in client.servers:
                for channel in server.channels:
                    try:
                        yield from sendMessage(channel, "Sorry I GTG, cya later...")
                    except discord.errors.HTTPException:
                        pass
            
            saveAndExit()
        
        if content.startswith(COMMAND_START + 'plot'):
            args = content.split(' ')
        
            
            try:
                
                expr = eval('lambda x: ' + args[1])
                xMin = float(args[2])
                xMax = float(args[3])
                yMin = float(args[4])
                yMax = float(args[5])
                
                if len(args) == 7:
                    step = float(args[6])
                
                else:
                    step = 0.01
                
                step = abs(step)
                
                print('Graphing from %f to %f' % (xMin, xMax))
                
                plt.clf()
                
                fig = plt.figure(1, figsize = (xMax - xMin, yMax - yMin))
                
                x = xMin
                
                ys = []
                
                while x < xMax:
                    ys.append(expr(x))
                    x += step
                
                def genRange (start, stop, step):
                    r = []
                    while start < stop:
                        r.append(start)
                        start += step
                    return r
                
                plt.plot(genRange(xMin, xMax, step), ys)
                
                fig.savefig('figure.png')
                
                yield from client.send_file(message.channel, str(os.path.curdir) + '/figure.png', content = str(xMin) + ' <= x < ' + str(xMax) + '\n' + str(yMin) + '<= y < ' + str(yMax))
            
            except:
                yield from sendMessage(message.channel, 'Sorry, I don\'t understand that...')
                
        if content.startswith(COMMAND_START + 'name'):
            NAMES[str(message.server.id)] = content.split(' ')[1]
            
            yield from client.change_nickname(message.server.me, content.split(' ')[1])
            
            save()

def sendMessage (channel, message):
    return client.send_message(channel, stutter(message))

def stutter (text):
    s = ''
    
    for i in text.split(' '):
        if random.random() <= float(DEFAULT['stutterRate']) and len(i) > 0 and len(i) < 10:
            if i[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                s += i[0] + '-' + i.lower() + ' '
        
        else:
            s += i + ' '
    
    return s

def saveAndExit ():
    save()
    exit()

def exit ():
    client.logout()
    sys.exit()

def save ():
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

client.run('MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk')