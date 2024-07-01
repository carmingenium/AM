import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands

description = '''Description test'''

TOKEN = os.environ["DISCORD_TOKEN"]
intents1 = Intents.all()

BOT = commands.Bot(command_prefix='!',description=description, intents=intents1)

@BOT.event
async def on_ready():
  print('Hello, I am ready!')

def main():
  print("I RAN")
  print("This is the token (secret): " + TOKEN)
  

  BOT.run(TOKEN)
main()