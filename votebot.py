import os
import time
import datetime
from datetime import datetime
import asyncio
from secrets import TOKEN
import random

import discord
import startvote

client = discord.Client()


channelName = "votechannel"
roleName = "Council"
limitChannel = False
limitRole = False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    if(message.author != client.user):
        guild = message.guild
        channel = message.channel
        if(not(limitChannel) or message.channel.name == channelName):
            roles = message.author.roles
            for role in roles:
                if(not(limitRole) or role.name == roleName):
                    await commands(message)
                    break

async def commands(message):
    content = message.content
    channel = message.channel
    if(content.startswith("!startvote")):
        await startvote.startVote(content[11:], channel)
    elif(content.startswith("!flip")):
        val = random.randint(0, 1) #generates either a 0 or a 1
        if(val == 0):
            await channel.send("Heads!")
        else:
            await channel.send("Tails!")
        


client.run(TOKEN)
