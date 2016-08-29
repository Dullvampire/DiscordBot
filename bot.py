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

import _thread as thread

import configparser

sleep(0.5)

EPOCH = datetime.datetime.utcfromtimestamp(0)
CLIENT_ID = '212451598352384002'
TOKEN = 'MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk'
COMMAND_START = '*'

config = configparser.ConfigParser()

config.read('settings.ini')

DEFAULT = config['DEFAULT']

client = discord.Client()

COMMAND_LIST = ['*help', '*restart', '*exit']
COMMANDS = {'*help' : 'Gives this!',
            '*restart' : 'Restarts L-lewdbot',
            '*exit' : 'Quits L-lewdbot'}

@client.async_event
def on_ready ():
    if len(client.servers) == 0:
        pass
    elif len(client.servers) == 1:
        print('Connected to ' + str(len(client.servers)) + " server!")
    else:
        print('Connected to ' + str(len(client.servers)) + " servers!")
    
    if DEFAULT['restart'] == 'false':
        for server in client.servers:
            yield from sendMessage(server.default_channel, "I-i'm here :heart:")
    
    else:
        ownersSentTo = []
        
        for server in client.servers:
            if server.owner not in ownersSentTo:
                yield from sendMessage(server.owner, "I was s-sucessfully restarted! I go to live another day")
                ownersSentTo.append(server.owner)
                
        DEFAULT['restart'] = 'false'
        
        save()

@client.async_event
def on_server_join (server):
    print('Joined ' + server.name)
    for channel in server.channels:
        try:
            yield from sendMessage(channel, "H-hello there, I am L-lewd bot :heart:")
        except discord.errors.HTTPException:
            pass

@client.async_event
def on_member_join (member):
    yield from sendMessage(member.server.default_channel, "H-hi " + member.display_name + " :heart:")

@client.async_event
def on_member_remove (member):
    yield from sendMessage(member.server.default_channel, "O-oh... W-was it m-my fault " + member.display_name + "? :broken_heart:")

@client.async_event
def on_member_update (before, after):
    if before.game == after.game and before.roles == after.roles and before.status == after.status:
        server = after.server
        yield from sendMessage(server.default_channel, "Hey " + before.display_name + " d-did you change s-something? You look different...")
        asyncio.sleep(10)
        yield from client.send_typing(server.default_channel)
        asyncio.sleep(3)
        changed = ''
        
        if before.display_name != after.display_name:
            changed = 'name, I l-like it a l-lot'
        
        elif before.avatar != after.avatar:
            changed = 'profile pick, looking fine as usual ' + after.display_name
            
        print(before.display_name, after.display_name)
        
        yield from sendMessage(server.default_channel, "Y-you did O.o your " + changed + '!')
    
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
                        yield from sendMessage(channel, "Sorry I GTG, c-cya later...")
                    except discord.errors.HTTPException:
                        pass
            
            saveAndExit()

def sendMessage (channel, message):
    return client.send_message(channel, message)

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