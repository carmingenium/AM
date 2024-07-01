import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = os.environ["DISCORD_TOKEN"]

@bot.event
async def on_ready():
  print('Hello, I am ready!')

def main():
  print("I RAN")
  if(TOKEN == None):
    print("The token is empty")
  else:
    print("This is the token (secret): " + TOKEN)
  
  bot = commands.Bot(command_prefix='!', intents=Intents.all())
  bot.run(TOKEN)
main()