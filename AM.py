import os
import discord
from discord.ext import commands
import asyncio
import time

# setup

BOT_TOKEN = os.environ["DISCORD_TOKEN"]
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
  # expire functionality
  await expire() # on ready gets stuck on here
  await dev_channel.send("Synced " + str(len(synced)) + " commands")

async def expire(): # this doesnt work currently.
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("Bot will shut down in 5 hours, 59 minutes")
  # normally shutdown happens after 6 hours, in 25 seconds.
  # We will shutdown at 5 hour 59 minutes 30 seconds to have 5 seconds of leeway.
  # New workflow will repeat every 6 hours
  await asyncio.sleep(5*60*60 + 59*60)  
  await dev_channel.send("Shutting down: " + str(bot.user) + " Reason: Expiration")
  await bot.close()

@bot.tree.command(name="help",description="Shows all usable commands")
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

@bot.event
async def on_disconnect():
  print("Bot is disconnected")


def main():
  bot.run(BOT_TOKEN)
main()


'''
SCHEDULE FILE SAVED HERE FOR LATER
name: Scheduled 6 Hour Repeat

on:
  schedule:
  - cron: '0 0,6,12,18 * * *'
env:
  DISCORD_TOKEN: ${{ secrets.DISCORD_TOKEN }}
jobs:

  run-code:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Version Check
        run: python --version
      - name: Install dependencies
        run:
          pip install discord
      - name: Run Bot
        run: 
          python AM.py
'''
