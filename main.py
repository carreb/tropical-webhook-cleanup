import discord
from discord import Embed
from discord.ext import commands, tasks
import asyncio
import pickle
import atexit
from time import sleep
import configparser

intcounter = 0
addtocounter = 0
loop = asyncio.get_event_loop()
BOT_PREFIX = ">"
bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

#setup config vars
config = configparser.ConfigParser()
config.read('config.ini')
info = config['info']
token = info['token']
redirectbool = info['redirectEnabled']
r = str(redirectbool).lower()
redirectchannel = info['redirectChannel']
with open("counter.txt", "r+") as f:
    counter = [i.strip() for i in f.readlines()][0]


channel = bot.get_channel(int(redirectchannel))


@tasks.loop(seconds = 30)
async def update():
    global intcounter
    global counter
    intcounter = int(counter) + addtocounter
    formatcounter = "{:,}".format(intcounter)
    await bot.change_presence(activity=discord.Game(name=f"{formatcounter} invalid pings removed"))
    print("Updated status! Now at" + "{:,}".format(intcounter))
    with open("counter.txt", "w+") as f:
        f.write(str(intcounter))


@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(redirectbool)
    print(redirectchannel)
    global channel
    channel = bot.get_channel(int(redirectchannel))
    print(channel)
    print('------')
    sleep(5)
    update.start()

@bot.event
async def on_message(message):
    global intcounter
    global addtocounter
    global channel
    embeds = message.embeds
    for embed in embeds:
        if "Rancher's Boots" in embed.description:
            if "#000000" in embed.fields[2].value:
                await message.delete()
                addtocounter += 1
                return
        elif r == "false":
            if message.author == bot.user:
                return
            else:
                redirectembed = discord.Embed(title=embed.title, description=embed.description, color=embed.color)
                redirectembed.add_field(name=embed.fields[0].name, value=embed.fields[0].value)
                redirectembed.add_field(name=embed.fields[1].name, value=embed.fields[1].value)
                redirectembed.add_field(name=embed.fields[2].name, value=embed.fields[2].value)
                redirectembed.set_footer(text="Tropical Cleanup Redirect")
                await channel.send(embed=redirectembed)
            
def exithandler():
    with open("counter.txt", "w+") as f:
        print("Saving and closing...")
        f.write(str(intcounter))

atexit.register(exithandler)

bot.run(token)
