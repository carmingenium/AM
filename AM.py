import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands



TOKEN = os.environ["DISCORD_TOKEN"]
BOT = commands.Bot(command_prefix='!', intents=Intents.all())

@BOT.event
async def on_ready():
  print('Hello, I am ready!')

def main():
  print("I RAN")
  print("This is the token (secret): " + TOKEN)
  

  BOT.run(TOKEN)
main()