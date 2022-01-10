import discord
from discord import Embed
from discord.ext import commands, tasks
import asyncio
import pickle
import atexit
from time import sleep

intcounter = 0
addtocounter = 0
loop = asyncio.get_event_loop()
BOT_PREFIX = ">"
bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

with open("bot_token.txt", "r+") as f:
	token = [i.strip() for i in f.readlines()][0]
with open("counter.txt", "r+") as f:
    counter = [i.strip() for i in f.readlines()][0]


@tasks.loop(seconds = 30)
async def update():
    global intcounter
    global counter
    intcounter = int(counter) + addtocounter
    await bot.change_presence(activity=discord.Game(name=f"{intcounter} invalid pings removed"))
    print("Updated status! Now at" + str(intcounter))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    sleep(5)
    update.start()

@bot.event
async def on_message(message):
    global intcounter
    global addtocounter
    embeds = message.embeds
    channel = bot.get_channel("930189197720047637")
    for embed in embeds:
        if "Rancher's Boots" in embed.description:
            if "#000000" in embed.fields[2].value:
                await message.delete()
                addtocounter += 1
                return
            
def exithandler():
    with open("counter.txt", "w+") as f:
        print("Saving and closing...")
        f.write(str(intcounter))

atexit.register(exithandler)

bot.run(token)
