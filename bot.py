'''
Discord Bot

To invite to server
https://discordapp.com/oauth2/authorize?client_id=212451598352384002&scope=bot&permissions=0
'''

#UTF-8 Encoding

import discord
import asyncio

CLIENT_ID = '212451598352384002'
TOKEN = 'MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk'
COMMAND_START = '*'

client = discord.Client()

@client.async_event
def on_ready ():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    print(client)

@client.async_event
def on_message (message):
    content = message.content
    
    if content.startswith(COMMAND_START + 'ping'):
        yield from client.send_message(message.channel, "Pong")
        print('recieved ping')

client.run('MjEyNDUxNTk4MzUyMzg0MDAy.CqU32g.2GURlLhFfdOtDWC9y_zGP1TAzqk')