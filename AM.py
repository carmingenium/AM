import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = os.environ["DISCORD_TOKEN"]


def main():
  print("I RAN")
  if(TOKEN == None):
    print("The token is empty")
  else:
    print("This is the token (secret): " + TOKEN)

main()


# @client.event
# async def on_ready():
#   print('Hello, I am ready!')