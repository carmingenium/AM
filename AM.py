import os
import discord
from discord.ext import commands
import asyncio
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta


# .env setup
load_dotenv()
BOT_TOKEN = os.getenv('KEY')
DB_URI = os.getenv("MONGO_URI")
DEV_CHANNEL = int(os.getenv("DEV_CHANNEL"))




# bot setup
intents1 = discord.Intents.all()
intents1.members = True
bot = commands.Bot(command_prefix='!', intents=intents1)
# db setup
mongo_client = MongoClient(DB_URI)
db = mongo_client["am_bot"]

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
               
@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
  await interaction.response.send_message("test command")


@bot.tree.command(name="setadmin", description="Sets an admin user for the bot.")
async def set_botadmin(interaction: discord.Interaction, user: discord.User, note: str = "dev"):
  # admin spesific
  admin_doc = db.admins.find_one({"user_id": str(interaction.user.id), "active": True})
  if admin_doc is None:
    await interaction.response.send_message("You are not an admin user.")
    return
  existing = False
  print_admins()
  try:
    existing = db.admins.find_one({"user_id": str(user.id)})
  except Exception as e:
    await interaction.response.send_message("An error occurred while checking the database.")
    return
  if existing:
    await interaction.response.send_message("This user is already an admin.")
    return

  db.admins.insert_one({
    "user_id": str(user.id),
    "username": str(user.name),
    "added_by": str(interaction.user.id),
    "added_at": (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(), # UTC+3 timezone
    "note": note,
    "active": True
  })
  await interaction.response.send_message(f"{user.mention} is now set as an admin.")


@bot.tree.command(name="terminate", description="Terminates bot.")
async def terminate(interaction: discord.Interaction):
  if str(interaction.user.id) not in db.admins.find_one({"user_id": str(interaction.user.id)})["user_id"]:
    await interaction.response.send_message("You are not an admin user.")
  else:
    await interaction.response.send_message("Terminating.")
    await bot.close()


@bot.event
async def on_disconnect():
  print("Bot is disconnected")

def print_admins():
  admins = db.admins.find({"active": True})
  admin_list = []
  for admin in admins:
    admin_list.append(f"{admin['user_id']} - {admin['username']} - {admin['note']}  ")
  print("Active Admins:")
  print("\n".join(admin_list) if admin_list else "No active admins found.")

def main():
  bot.run(BOT_TOKEN)
main()