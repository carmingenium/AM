import os
import discord
from discord.ext import commands
import asyncio
import time
from dotenv import load_dotenv

# setup
load_dotenv()
BOT_TOKEN = os.getenv('KEY')
DEV_CHANNEL = 1267387974350405700 # make this settable for every server later on
intents1 = discord.Intents.all()
intents1.members = True
bot = commands.Bot(command_prefix='!', intents=intents1)
# setup end
global dev_channel



@bot.event
async def on_ready(): # quick note, on_ready is called whenever resume fails
  print("bot is active")
  print(f'{bot.user} has connected to Discord!')
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT ACTIVE")
  synced = await bot.tree.sync()
  print("synced" + str(len(synced)))
  await dev_channel.send("Synced " + str(len(synced)) + " commands")

@bot.tree.command(name="help",description="Shows all usable commands") # needs to be implemented
async def help(interaction: discord.Interaction):
  # learn about different displays
  await interaction.response.send_message("Not implemented yet")
  # returns empty list
  # await interaction.response.send_message("Here are all the commands: " + str(all_commands))

@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
  await interaction.response.send_message("test command")

@bot.tree.command(name="shutdown", description="Shuts down the bot.")
async def close_bot(interaction: discord.Interaction):
  await interaction.response.send_message("Shutting down: " + str(bot.user) + " Reason: Force Shutdown")
  await bot.close()
  
  
# calendar style popup menu for picking a date. multiple people can pick a date, and the bot will keep track of who picked what date.
# also need to learn about databases

@bot.event
async def on_disconnect():
  print("Bot is disconnected")


def main():
  bot.run(BOT_TOKEN)
main()