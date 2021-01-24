import os
import time
import datetime
from datetime import datetime
import asyncio

import discord

emojis = ['👍', '👎']

async def startVote(content, channel):
    title = ""
    description = ""
    userTime = "0"
    info = []
    if(len(content) > 0 and content[0] == "\""):
        info = readString(content)
    else:
        if(len(content) > 0):
            info.append(content)
        else:
            info.append("Vote")
    if(len(info) > 0):
        title = info[0]
    if(len(info) == 3):
        description = info[1]
    if(len(info) >= 2):
        if(len(info) == 2):
            userTime = info[1]
        else:
            userTime = info[2]
    else:
        userTime = "0"

    userTime = parseTime(userTime)
    print("Vote started: " + str(info) + " in channel \"" + channel.name + "\" in guild \"" + channel.guild.name + "\"")


    embed = discord.Embed(title=title, color=0xFFFF00)
    if(description != "" and description != " "):
        embed.add_field(name='Description', value=description, inline=False)
    if(userTime > 0):
        embed.add_field(name='Time Limit', value=findTimeProper(userTime) + " from " + str(datetime.now()), inline=False)
    newMessage = (await channel.send(embed=embed))
    for emoji in emojis:
        await newMessage.add_reaction(emoji)

    if(userTime > 0):
        await asyncio.sleep(userTime)

        newMessage = await channel.fetch_message(newMessage.id)

        yes = -1
        no = -1
        for reaction in newMessage.reactions:
            if(reaction.emoji == emojis[0]):
                yes += reaction.count
            elif(reaction.emoji == emojis[1]):
                no += reaction.count
        if(yes > no):
            embed = discord.Embed(title=title, color=0x00FF00)
            if(description != "" and description != " "):
                embed.add_field(name='Description', value=description, inline=False)
            embed.add_field(name='PASSED', value="\u200b", inline=True)
        else:
            embed = discord.Embed(title=title, color=0xFF0000)
            if(description != "" and description != " "):
                embed.add_field(name='Description', value=description, inline=False)
            embed.add_field(name='REJECTED', value="\u200b", inline=True)

        await channel.send(embed=embed)


def readString(content):
    info = []
    content = content[1:]
    for i in range(0,3):
        index = content.find("\"")
        if(index != -1):
            info.append(content[:index])
            content = content[index:]
            while(len(content) > 0 and (content[0] == " " or content[0] == "\"")):
                content = content[1:]
        else:
            if(len(content) > 0):
                info.append(content)
            break
    return info

def parseTime(time):
    unit = time[len(time) - 1]
    if(unit.isalpha()):
        amount = time[:(len(time) - 1)]
    else:
        amount = time[:len(time)]
    finalTime = 0
    if(amount.isnumeric() and unit.isalpha()):
        amount = int(amount)
        if(unit == 'm'):
            finalTime = amount * 60
        elif(unit == 'h'):
            finalTime = amount * 60 * 60
        elif(unit == 'd'):
            finalTime = amount * 60 * 60 * 24
        elif(unit == 'w'):
            finalTime = amount * 60 * 60 * 24 * 7
        else:
            finalTime = amount
    elif(amount.isnumeric()):
        finalTime = amount
    return int(finalTime)

def findTimeProper(amount):
    units = str(amount) + " seconds"
    if(amount >= 60*60*24*7):
        units = str(amount/60/60/24/7) + " weeks"
    elif(amount >= 60*60*24):
        units = str(amount/60/60/24) + " days"
    elif(amount >= 60*60):
        units = str(amount/60/60) + " hours"
    elif(amount >= 60):
        units = str(amount/60) + " minutes"
    return units