# Unite Bot - Server (v1.0)
# Created by James Borgars

# Imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import pickle

# Account Class
class Account:
    def __init__(self, name):
        self.user = name
        self.steam = "None"
        self.origin = "None"
        self.uplay = "None"
        self.battlenet = "None"

# Grabbing Database
with open('users', 'rb') as fp:
    hashTable = pickle.load(fp)
print("Hash Table Loaded...\n")

# Necessary Client & Token Declaration
client = Bot(description="μnite by jdb#3386", command_prefix="//", pm_help = True)
token = "Mzk0ODcwMzk2MDUyMTc2ODk2.DSKwrw.s9xGULrDAa9ByktgWZB7fnWH8v4"

# Bot Launching Information
@client.event
async def on_ready():
    print('Bot Launched...')
    print('\n\nBOT INFO')
    print('Bot Name: '+ client.user.name)
    print('Bot ID: '+ client.user.id)
    print('No. of Server Connections: '+ str(len(client.servers)))
    print('\n\nENVIRONMENT INFO')
    print('Discord.py Version: ' + discord.__version__)
    print('Python Version: ' + platform.python_version())
    print('\n\nINVITE LINK')
    print('https://discordapp.com/oauth2/authorize?client_id=' + client.user.id + '&scope=bot&permissions=8')
    print('\n\nThis bot was created by James Borgars')
    await client.change_presence(game=discord.Game(name='μnite | Say //faq'))

# Commands
@client.command(pass_context=True)
async def create(ctx):
    discordName = str(ctx.message.author)
    discordSplit = discordName.rsplit("#")
    discordID = int(discordSplit[len(discordSplit)-1])
    newAccount = Account(discordName)
    if hashTable[discordID] == "":
        hashTable[int(discordID)] = [newAccount]
        await client.say('User ' + discordName + ' added to database.')
        with open('users', 'wb') as fp:
            pickle.dump(hashTable, fp)
        print("[INFO] User",discordName,"added to database.")
    else:
        identical = False
        for x in range(len(hashTable[discordID])):
            if hashTable[discordID][x].user == newAccount.user:
                identical = True
                await client.say('User ' + discordName + ' is already in database! Use //add to add Usernames to this account.')
                break
        if not identical:
            hashTable[discordID].append(newAccount)
            await client.say('User ' + discordName + ' added to database.')
            with open('users', 'wb') as fp:
                pickle.dump(hashTable, fp)
            print("[INFO] User",discordName,"added to database.")

@client.command(pass_context=True)
async def add(ctx, game : str, uid):
    discordName = str(ctx.message.author)
    discordSplit = discordName.rsplit("#")
    discordID = int(discordSplit[len(discordSplit)-1])
    if hashTable[discordID] == "":
        await client.say('User ' + discordName + ' not found in database! Use //create to add to database.')
    else:
        found = False
        for x in range(len(hashTable[discordID])):
            if hashTable[discordID][x].user == discordName:
                found = True
                userLocation = x
        if not found:
            await client.say('User ' + discordName + ' not found in database! Use //create to add to database.')
        else:
            if game.lower() == "steam":
                hashTable[discordID][userLocation].steam = str(uid)
                await client.say('User ' + discordName + ' added a Steam ID to the database.')
            if game.lower() == "origin":
                hashTable[discordID][userLocation].origin = str(uid)
                await client.say('User ' + discordName + ' added an Origin ID to the database.')
            if game.lower() == "uplay":
                hashTable[discordID][userLocation].uplay = str(uid)
                await client.say('User ' + discordName + ' added a uPlay ID to the database.')
            if game.lower() == "battlenet":
                hashTable[discordID][userLocation].battlenet = str(uid)
                await client.say('User ' + discordName + ' added a Battle.net ID to the database.')
            with open('users', 'wb') as fp:
                pickle.dump(hashTable, fp)
            print("[INFO] User",discordName + "'s profile modified.")

@client.command()
async def show(username):
    discordName = username
    discordSplit = discordName.rsplit("#")
    discordID = int(discordSplit[len(discordSplit)-1])
    if hashTable[discordID] == "":
        await client.say('User ' + discordName + ' not found in database!')
    else:
        found = False
        for x in range(len(hashTable[discordID])):
            if hashTable[discordID][x].user == discordName:
                found = True
                userLocation = x
        if not found:
            await client.say('User ' + discordName + ' not found in database!')
        else:
            await client.say('Discord User **`' + discordName + '`**:\nSteam ID: **`' + hashTable[discordID][userLocation].steam + '`**\nOrigin ID: **`' + hashTable[discordID][userLocation].origin + '`**\nuPlay ID: **`' + hashTable[discordID][userLocation].uplay + '`**\nBattle.net ID: **`' + hashTable[discordID][userLocation].battlenet + '`**')

@client.command()
async def about(*args):
    serverNum = str(len(client.servers))
    await client.say('`About μnite`\nVersion: 1.0\nCreated By: jdb#3386\nConnected to ' + serverNum + ' different servers!\n **` \nUSE //donate FOR DONATION INFORMATION`**')

@client.command()
async def faq(*args):
    await client.say('μnite Help:\n`//create` - Adds the user who calls the command to the μnite database\n`//add [PLATFORM] [ID]` - Adds a platform ID to the called user (Platforms supported: `steam`,`origin`,`uplay`,`battlenet`)\n`//show [DISCORD ID]` - Shows the IDs stored in the μnite database for a discord user.')

@client.command()
async def donate(*args):
    await client.say('Donation information coming soon!')
# Starting Bot
client.run(token)
            
