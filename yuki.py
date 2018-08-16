import discord
from discord.ext import commands

import logging
import sys, traceback

import webcolors
from os.path import isfile
from configparser import RawConfigParser

import aiohttp
import asyncio

description = '''A multi-purpose bot with fun commands'''
prefix = ".yk "

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(prefix), # , u"\U0001f916"),
    description = description,
    owner_id = 393041441301200896
)
bot.remove_command("help")
color = 0xFF033E

initial_extensions = (
    "cogs.owner",
    "cogs.image",
    "cogs.text",
    "cogs.guild",
    "cogs.info",
    "cogs.tests",
    "cogs.utils",
    "cogs.coins",
    "cogs.copypasta"
)
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {extension}.", file = sys.stderr)
        traceback.print_exc()

@bot.event  
async def on_ready():
    logging.info("Logged in as")
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info("------")

    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers. | {prefix}help"))

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers. | {prefix}help"))

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers. | {prefix}help"))

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.author.bot:
        return

    await bot.process_commands(msg)

async def getImage(link, ctx):
    if link == None: # If no link is passed
        if len(ctx.message.attachments) >= 1:
            # Attachment
            usedLink = ctx.message.attachments[0].url
        else:
            # Last Attachment

            a = []
            async for message in ctx.channel.history(limit = 10):
                if len(message.attachments) >= 1:
                    a.append(message.attachments[-1])
            if len(a) != 0:
                usedLink = a[-1].url # Set link to the last attachment url in the list
            else:
                usedLink = link
    elif link.startswith("<:"): # (Custom) Emoji
        id = link.split(':')[2][:-1]
        usedLink = bot.get_emoji(id).url
        print(id, usedLink)
    else:
        usedLink = link

    async with aiohttp.ClientSession() as clientSession:  # Link
        async with clientSession.get(usedLink) as response:
            return await response.read()

async def startTyping(channelID):
    cha = await bot.get_channel(id = int(channelID))
    await cha.trigger_typing()

def runBot():
    if isfile("config.ini"):
        config = RawConfigParser()
        config.read("config.ini")
        token = config["Secret"]["bot_token"]
    else:
        config = RawConfigParser()
        token = input("Type in your bot token: ")
        config.add_section("Secret")
        config["Secret"]["bot_token"] = token
        with open("config.ini", "w") as f:
            config.write(f)

    bot.run(token, bot = True, reconnect = True)

if __name__ == "__main__":
    runBot()
