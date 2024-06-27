import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
from discord.ext import commands
import discord

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = os.environ["DISCORD_TOKEN"]



@client.event
async def on_ready():
  print('Hello, I am ready!')