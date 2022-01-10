import discord
from discord import Embed
from discord.ext import commands
import asyncio



loop = asyncio.get_event_loop()
BOT_PREFIX = ">"
bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

with open("bot_token.txt", "r+") as f:
	token = [i.strip() for i in f.readlines()][0]


@bot.event
async def on_message(message):
    embeds = message.embeds
    for embed in embeds:
        if "Rancher's Boots" in embed.description:
            if "#000000" in embed.fields[2].value:
                await message.delete()


bot.run(token)
