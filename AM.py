import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands
import ssl # needed for certification ?? (testing)


# setup
description = '''Description test'''
TOKEN = os.environ["DISCORD_TOKEN"]
intents1 = Intents.all()
BOT = commands.Bot(command_prefix='!',description=description, intents=intents1)
# setup end

@BOT.event
async def on_ready():
  print('Hello, I am ready!')

def main():
  print("I RAN")
  print("This is the token (secret): " + TOKEN)
  
  ssl._create_default_https_context = ssl._create_unverified_context # needed for certification ?? (testing)

  BOT.run(TOKEN) # this is where the bot gets stuck
  # Bot does not run on_ready command when it runs
main()