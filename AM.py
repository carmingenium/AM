import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands


# setup
description = '''Description test'''
TOKEN = os.environ["DISCORD_TOKEN"]
intents1 = Intents.all()
BOT = commands.Bot(command_prefix='!',description=description, intents=intents1)
# setup end

@bot.event
async def on_ready():
  print("bot is active")
  print(f'{bot.user} has connected to Discord!')
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT ACTIVE")
  
@bot.event
async def on_disconnect():
  print("bot is disconnected")
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT DISCONNECTED")

@bot.command(name='test')
async def test(ctx):
  await bot.close()












def main():
  bot.run(BOT_TOKEN)
main()
