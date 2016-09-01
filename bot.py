'''
Discord Bot

To invite to server
https://discordapp.com/oauth2/authorize?client_id=220619851243192320&scope=bot&permissions=12659727
'''

#UTF-8 Encoding

import discord
import asyncio
import time
import sys
import os
import datetime

import numpy as np

import _thread as thread

from matplotlib import pyplot as plt
from matplotlib import pylab as pyl
import random

import configparser
from flask.helpers import send_file
from math import *

time.sleep(0.5)

def _checkStutterRate (s):
    try:
        float(s)
        return True
    except:
        return False

EPOCH = datetime.datetime.utcfromtimestamp(0)
CLIENT_ID = '212451598352384002'
TOKEN = 'MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk'
COMMAND_START = '*'

config = configparser.ConfigParser()

config.read('settings.ini')

defaults = configparser.ConfigParser()

defaults.read('defaults.ini')

client = discord.Client()

NAME = 'Rivenbot'

COMMAND_LIST = ['*help', '*restart', '*exit', '*update', '*plot', '*joinme', '*leaveme', '*name', '*play', '*pause', '*resume', '*stop', '*queue', '*skip', '*volume']
COMMANDS = {'*help' : 'Gives this!',
            '*restart' : 'Restarts ' + NAME,
            '*exit' : 'Quits ' + NAME,
            '*update' : 'Pulls update from github',
            '*plot' : 'Plots a function, usage: *plot <function in form of y=f(x)> <minX> <maxX> <step>',
            '*joinme' : NAME + ' joins your voice channel',
            '*leaveme' : NAME + ' leaves your voice channel',
            '*name' : 'Sets the nickname of the bot',
            '*play' : 'Plays a youtube video in the form *play <url>',
            '*pause' : 'Pauses current youtube video',
            '*resume' : 'Resumes current youtube video',
            '*stop' : 'Stops current video and clears queue', 
            '*queue' : 'lists queue',
            '*skip' : 'skips current video',
            '*volume' : 'sets volume for videos, between 0 and 1'}

SETTINGS = {'DEFAULT' : {'restart' : lambda x: False,
                         'stutterRate' : _checkStutterRate}}

RUNTIME_VARIABLES = {'voice' : {},
                     'players' : {},
<<<<<<< HEAD
                     'volume' : {}}
=======
                     'volume' : {},
                     'start' : time.time()}
>>>>>>> master

@client.async_event
def on_ready ():
    for server in client.servers:
        if str(server.id) in config['NAMES']:
            yield from client.change_nickname(server.me, config['NAMES'][str(server.id)])
        else:
            yield from client.change_nickname(server.me, NAME)
        
        for i in defaults['DEFAULT']:
            if i not in config[str(server.id) + 'DEFAULT'].keys():
                config[str(server.id) + 'DEFAULT'][i] = defaults['DEFAULT'][i]
        
        
        for i in defaults['VOICE']:
            if i not in config[str(server.id) + 'VOICE'].keys():
                config[str(server.id) + 'VOICE'][i] = defaults['VOICE'][i]
        
        RUNTIME_VARIABLES['players'][server.id] = []
        
        RUNTIME_VARIABLES['volume'][server.id] = float(config[str(server.id) + 'DEFAULT']['volume'])
    
    if len(client.servers) == 0:
        pass
    elif len(client.servers) == 1:
        print('Connected to ' + str(len(client.servers)) + " server!")
    else:
        print('Connected to ' + str(len(client.servers)) + " servers!")
    
    for server in client.servers:
        if config[str(server.id) + 'DEFAULT']['restart'] == 'false':
            yield from sendMessage(server.default_channel, getLine(server.id, 'entryMessage'))

    else:
        ownersSentTo = []
        
        for server in client.servers:
            if server.owner not in ownersSentTo:
                yield from sendMessage(server.owner, getLine(server.id, 'restarted'))
                ownersSentTo.append(server.owner)
            
                config[str(server.id) + 'DEFAULT']['restart'] = 'false'
        
        save()

@client.async_event
def on_server_join (server):
    print('Joined ' + server.name)
    for channel in server.channels:
        try:
            yield from sendMessage(channel, getLine(server.id, 'serverJoined'))
        except discord.errors.HTTPException:
            pass

@client.async_event
def on_member_join (member):
    yield from sendMessage(member.server.default_channel, getLine(member.server.id, 'memberJoin'))

@client.async_event
def on_member_remove (member):
    yield from sendMessage(member.server.default_channel, getLine(member.server.id, 'memberLeave'))

@client.async_event
def on_member_update (before, after):
    if after != after.server.me:
        if before.game == after.game and before.roles == after.roles and before.status == after.status:
            server = after.server
            yield from sendMessage(server.default_channel, getLine(member.server.id, 'memberUpdate'))
            asyncio.sleep(10)
            yield from client.send_typing(server.default_channel)
            asyncio.sleep(3)
            changed = ''
            
            if before.display_name != after.display_name:
                changed = getLine(member.server.id, 'nameUpdated')
            
            elif before.avatar != after.avatar:
                changed = getLine(member.server.id, 'picUpdated') + after.display_name
                
            print(before.display_name, after.display_name)
            
            yield from sendMessage(server.default_channel, getLine(member.server.id, 'updateRealize') + changed + '!')
    
@client.async_event
def on_message (message):
    content = message.content
    
    try:
        sID = str(message.server.id)
    except:
        pass
    
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
        
        if content.startswith(COMMAND_START + 'set') and message.author.id == message.server.owner.id:
            try:
                args = content.split(' ')
                
                if setConfig(message.server.id, args[1], *args[2:]):
                    save()
                else:
                    raise ValueError
                
                yield from sendMessage(message.channel, getLine(sID, 'setSettingChanged'))
            
            except:
                yield from sendMessage(message.channel, getLine(sID, 'setSettingFailed'))
        
        if content.startswith(COMMAND_START + 'reset') and message.author.id == message.server.owner.id:
            try:
                args = content.split(' ')
                
                if resetConfig(message.server.id, *args[1:]):
                    save()
                else:
                    raise ValueError
                
                yield from sendMessage(message.channel, getLine(sID, 'setSettingChanged'))
            
            except:
                yield from sendMessage(message.channel, getLine(sID, 'failure'))
        
        if content.startswith(COMMAND_START + 'restart'):
            if isAdmin(message.author):
                for server in client.servers:
                    for channel in server.channels:
                        try:
                            yield from sendMessage(channel, getLine(sID, 'restart'))
                        except discord.errors.HTTPException:
                            pass
                
                for serverID in config:
                    config[str(server.id) + 'DEFAULT']['restart'] = 'true'
                    
                
                for i in RUNTIME_VARIABLES['voice'].keys():
                    if RUNTIME_VARIABLES['voice'][i] != None:
                        yield from RUNTIME_VARIABLES['voice'][i].disconnect()
                        RUNTIME_VARIABLES['voice'][i] = None
                
                save()
                thread.start_new_thread(os.system, ('run.bat',))
                exit()
            
            else:
                yield from sendMessage(message.channel, getLine(sID, 'admin'))
        
        if content.startswith(COMMAND_START + 'update'):
            if isAdmin(message.author):
                for server in client.servers:
                    for channel in server.channels:
                        try:
                            yield from sendMessage(channel, getLine(sID, 'update'))
                        except discord.errors.HTTPException:
                            pass
                
                for i in RUNTIME_VARIABLES['voice'].keys():
                    if RUNTIME_VARIABLES['voice'][i] != None:
                        yield from RUNTIME_VARIABLES['voice'][i].disconnect()
                        RUNTIME_VARIABLES['voice'][i] = None
                
                save()
                os.system('update.bat')
                thread.start_new_thread(os.system, ('run.bat',))
                exit()
            
            else:
                yield from sendMessage(message.channel, getLine(sID, 'admin'))
        
        if content.startswith(COMMAND_START + 'exit'):
            if isAdmin(message.author):
                for server in client.servers:
                    for channel in server.channels:
                        try:
                            yield from sendMessage(channel, getLine(sID, 'exit'))
                        except discord.errors.HTTPException:
                            pass
                
                for i in RUNTIME_VARIABLES['voice'].keys():
                    if RUNTIME_VARIABLES['voice'][i] != None:
                        yield from RUNTIME_VARIABLES['voice'][i].disconnect()
                        RUNTIME_VARIABLES['voice'][i] = None
                
                saveAndExit()
            
            else:
                yield from sendMessage(message.channel, getLine(sID, 'admin'))
        
        if content.startswith(COMMAND_START + 'plot'):
            
            args = content.split(' ')
        
            
            try:
                
                expr = eval('lambda x: ' + args[1])
                xMin = float(args[2])
                xMax = float(args[3])
                
                if len(args) == 5:
                    step = float(args[4])
                
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
                yield from sendMessage(message.channel, getLine(sID, 'dontUnderstand'))
                
        if content.startswith(COMMAND_START + 'name'):
            config['NAMES'][str(message.server.id)] = content.split(' ')[1]
            
            yield from client.change_nickname(message.server.me, content.split(' ')[1])
            
            save()
        
        if content.startswith(COMMAND_START + 'joinme') or content.startswith(COMMAND_START + 'cometome'):
            try:
                RUNTIME_VARIABLES['voice'][message.server.id] = yield from client.join_voice_channel(message.author.voice_channel)
                yield from sendMessage(message.channel, getLine(sID, 'joinSuccess'))
            except:
                yield from sendMessage(message.channel, getLine(sID, 'joinFailure'))
        
        if content.startswith(COMMAND_START + 'leaveme'):
            if RUNTIME_VARIABLES['voice'][message.server.id] != None:
                yield from RUNTIME_VARIABLES['voice'][message.server.id].disconnect()
                RUNTIME_VARIABLES['voice'][message.server.id] = None
                yield from sendMessage(message.channel,  getLine(sID, 'leaveSuccess'))
            
            else:
                yield from sendMessage(message.channel, getLine(sID, 'leaveFailure'))
<<<<<<< HEAD
=======
        
        if content.startswith(COMMAND_START + 'status'):
            yield from sendMessage(message.channel, 'I\'ve been up for ' + str(time.time() - RUNTIME_VARIABLES['start']) + ' seconds')
>>>>>>> master
        
        if content.startswith(COMMAND_START + 'play'):
            url = content.split(' ')
            nURL = []
            
<<<<<<< HEAD
            if message.server.id in RUNTIME_VARIABLES['players'].keys():
                if type(RUNTIME_VARIABLES['players'][message.server.id]) == list:
                    player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                    RUNTIME_VARIABLES['players'][message.server.id].append(player)
                    player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                    player.start()
                else:
                    RUNTIME_VARIABLES['players'][message.server.id] = []
                    player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                    RUNTIME_VARIABLES['players'][message.server.id].append(player)
                    player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                    player.start()
            else:
                RUNTIME_VARIABLES['players'][message.server.id] = []
                if message.server.id in RUNTIME_VARIABLES['voice'].keys():
                    player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                    RUNTIME_VARIABLES['players'][message.server.id].append(player)
                    player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                    player.start()
                else:
                    player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                
                    player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                    
                    player.start()
                
                    RUNTIME_VARIABLES['players'][message.server.id].append(player)
            
            if len(RUNTIME_VARIABLES['players'][message.server.id]) > 0 and not RUNTIME_VARIABLES['players'][message.server.id][0].is_playing():
                RUNTIME_VARIABLES['players'][message.server.id][0].start()
                yield from sendMessage(message.channel, 'Playing: ' + RUNTIME_VARIABLES['players'][message.server.id][0].title)
=======
            for i in url:
                if i != '':
                    nURL.append(i)
            
            url = nURL[1]
            
            try:
                if message.server.id in RUNTIME_VARIABLES['players'].keys():
                    if type(RUNTIME_VARIABLES['players'][message.server.id]) == list:
                        player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                        RUNTIME_VARIABLES['players'][message.server.id].append(player)
                        player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                        
                        if len(RUNTIME_VARIABLES['players'][message.server.id]) == 1:
                            player.start()
                    else:
                        RUNTIME_VARIABLES['players'][message.server.id] = []
                        player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                        RUNTIME_VARIABLES['players'][message.server.id].append(player)
                        player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                        player.start()
                else:
                    RUNTIME_VARIABLES['players'][message.server.id] = []
                    if message.server.id in RUNTIME_VARIABLES['voice'].keys():
                        player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                        RUNTIME_VARIABLES['players'][message.server.id].append(player)
                        player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                        player.start()
                    else:
                        player = yield from RUNTIME_VARIABLES['voice'][message.server.id].create_ytdl_player(url)
                    
                        player.volume = RUNTIME_VARIABLES['volume'][message.server.id]
                        
                        player.start()
                    
                        RUNTIME_VARIABLES['players'][message.server.id].append(player)
                
                if len(RUNTIME_VARIABLES['players'][message.server.id]) > 0 and not RUNTIME_VARIABLES['players'][message.server.id][0].is_playing():
                    RUNTIME_VARIABLES['players'][message.server.id][0].start()
                    yield from sendMessage(message.channel, 'Playing: ' + RUNTIME_VARIABLES['players'][message.server.id][0].title)
            except:
                yield from sendMessage(message.channel, getLine(sID, 'leaveFailure'))
>>>>>>> master
        
        if content.startswith(COMMAND_START + 'stop'):
            if message.server.id in RUNTIME_VARIABLES['players'] and RUNTIME_VARIABLES['players'][message.server.id] not in [[], None]:
                RUNTIME_VARIABLES['players'][message.server.id].pop(0).stop()
<<<<<<< HEAD
                yield from sendMessage(message.content, "Stopping")
=======
                yield from sendMessage(message.channel, "Stopping")
>>>>>>> master
                RUNTIME_VARIABLES['players'][message.server.id] = []
        
        if content.startswith(COMMAND_START + 'pause'):
            if message.server.id in RUNTIME_VARIABLES['players'] and RUNTIME_VARIABLES['players'][message.server.id] not in [[], None]:
                RUNTIME_VARIABLES['players'][message.server.id][0].pause()
                yield from sendMessage(message.channel, "Pausing: " + RUNTIME_VARIABLES['players'][message.server.id][0].title)
        
        if content.startswith(COMMAND_START + 'resume'):
            if message.server.id in RUNTIME_VARIABLES['players'] and RUNTIME_VARIABLES['players'][message.server.id] not in [[], None]:
                RUNTIME_VARIABLES['players'][message.server.id][0].resume()
                yield from sendMessage(message.channel, "Resuming: " + RUNTIME_VARIABLES['players'][message.server.id][0].title)
        
        if content.startswith(COMMAND_START + 'queue'):
            if len(RUNTIME_VARIABLES['players'][message.server.id]) == 0:
                yield from sendMessage(message.channel, getLine(sID, 'noSongs'))
            
            else:    
                for i, j in enumerate(RUNTIME_VARIABLES['players'][message.server.id]):
                    yield from sendMessage(message.channel, "%i - %s" % (i + 1, j.title))
        
        if content.startswith(COMMAND_START + 'skip'):
            if len(RUNTIME_VARIABLES['players'][message.server.id]) == 0:
                yield from sendMessage(message.channel, getLine(sID, 'noSongs'))
            
            else:
                RUNTIME_VARIABLES['players'][message.server.id][0].stop()
                
                RUNTIME_VARIABLES['players'][message.server.id].pop(0)
                
                if len(RUNTIME_VARIABLES['players'][message.server.id]) > 0:
                    RUNTIME_VARIABLES['players'][message.server.id][0].start()
        
        if content.startswith(COMMAND_START + 'volume'):
            if len(content.split(' ')) == 1:
                yield from sendMessage(message.channel, getLine(sID, 'notEnoughArgs'))
                
            else:
                vol = float(content.split(' ')[1])
                for i in RUNTIME_VARIABLES['players'][message.server.id]:
                    i.volume = vol
                
                RUNTIME_VARIABLES['volume'][message.server.id] = vol

def sendMessage (channel, message):
    return client.send_message(channel, stutter(message, channel.server))

def stutter (text, server):
    s = ''
    
    for i in text.split(' '):
        if random.random() <= float(config[str(server.id) + 'DEFAULT']['stutterRate']) and len(i) > 0 and len(i) < 10:
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
    f = open('settings.ini', 'w')
    with f as configfile:
        config.write(configfile)
    
    f.close()

def isAdmin (member):
    f = open('systemAdmins.txt', 'r')
    for i in f.readlines():
        if i == str(member.id):
            f.close()
            return True
    
    f.close()
    
    return False

def setConfig (serverID, value, *arg):
    serverID = str(serverID)
    
    try:
        c = config[serverID + arg[0]]
        
        for i in arg[1:-1]:
            c = c[i]
            
        c[arg[-1]] = value
        
        return True
    except:
        return False

def readConfig (file, *arg):
    c = file[arg[0]]
    
    for i in arg[1:]:
        c = c[i]
    
    return c

def resetConfig (serverID, *arg):
    serverID = str(serverID)
    
    try:
        setConfig(serverID, readConfig(defaults, *arg), *arg)
        print('reset')
        return True
    except:
        return False

def setGlobalConfig (value, *arg):
    try:
        for serverID in config:
            c = config[serverID + arg[0]]
            
            for i in arg[1:-1]:
                c = c[i]
                
            c[arg[-1]] = value
        
        return True
    except:
        return False

def getLine (serverID, code):
    return config[str(serverID) + 'VOICE'][code]

<<<<<<< HEAD
client.run('MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk')
=======
client.run('MjIwNjE5ODUxMjQzMTkyMzIw.Cqi7xA.HjOHCP0gp0GQCqPZVJevxGIV2JM')
>>>>>>> master
