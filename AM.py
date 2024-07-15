import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands


# setup
description = '''Description test'''
TOKEN = os.environ["DISCORD_TOKEN"]
intents1 = Intents.all()
bot = commands.Bot(command_prefix='!',description=description, intents=intents1)
# setup end

@bot.event
async def on_ready():
  print("bot is active")
  print(f'{bot.user} has connected to Discord!')
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT ACTIVE")
  
@bot.command(name='close')
async def close_bot(ctx):
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT DISCONNECTED")
  await bot.close()

# Handling on_disconnect() event (optional)
@bot.event
async def on_disconnect():
  print("Bot is disconnected")  # This will print to console when disconnected
  # You may choose to send a message here as well, but remember it won't trigger on bot.close()












def main():
  bot.run(BOT_TOKEN)
main()
