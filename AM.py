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
  await interaction.followup.send(f"{user.mention} is now set as an admin.")


@bot.tree.command(name="terminate", description="Terminates bot.")
async def terminate(interaction: discord.Interaction):
  admin_doc = db.admins.find_one({"user_id": str(interaction.user.id), "active": True})
  if admin_doc is None:
    await interaction.response.send_message("You are not an admin user.")
    return
  else:
    await interaction.response.send_message("Terminating.")
    await bot.close()

@bot.tree.command(name="createevent", description="Starts a sequence to create a poll for an online event.")
async def event_poll(interaction: discord.Interaction):
  # get "events" until stop
  # respond in the interaction channel
  await interaction.response.send_message("Starting event creation sequence. Please provide the event names one by one. Type 'stop' to finish.")
  event_list = []
  time_list = []
  while True:
    try:
      await interaction.followup.send("Add an event.")
      msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
      if (msg.content.lower() == 'stop'):
        if not event_list:
          await interaction.followup.send("No events were provided. Cancelling event creation.")
          return
        break
      await interaction.followup.send(f"{msg.content} added to the event list, are you sure? Type 'no' to cancel, 'yes' to confirm.")
      response = await bot.wait_for('message', timeout=15.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
      if(response.content.lower() == 'no'):
        await interaction.followup.send(f"{msg.content} was not added to the event list. Please type another event or 'stop' to finish.")
        continue
      elif(response.content.lower() == 'yes'):
        await interaction.followup.send(f"{msg.content} was added to the event list.")
      else:
        await interaction.followup.send("Invalid response. Please type 'yes' to confirm or 'no' to cancel.")
        continue
    except asyncio.TimeoutError:
      await interaction.followup.send("Event creation timed out. Please start again.")
      return
    event_list.append(msg.content) # event added
    
    
  # get "time" for every event until stop
  for event in event_list:
    await interaction.followup.send(f"Please provide the time for the event '{event}'. Type 'stop' to finish.")
    time_currentlist = []
    while True:
      try:
        time_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
        if time_msg.content.lower() == 'stop':
          if not time_currentlist:
            await interaction.followup.send("No times were provided. Cancelling event creation.")
            return
          time_list.append(time_currentlist)
          break
        await interaction.followup.send(f"Time '{time_msg.content}' added for event '{event}'.")
        time_currentlist.append(time_msg.content)  # time added
      except asyncio.TimeoutError:
        await interaction.followup.send("Time input timed out. Please start again.")
        return



  await interaction.followup.send("Event creation complete. Here are the events you provided:")   # confirm the events and times
  await interaction.followup.send("\n".join(event_list))   # display
  for event in event_list:
    current = f"Event: {event} \t Times: "
    for time in time_list[event_list.index(event)]:
      current += f"{time}, "
    await interaction.followup.send(current)

  await interaction.followup.send("Any changes you want to make? Type 'yes' to edit, 'no' to confirm.") # remove by index add to the end
  if(await bot.wait_for('message', timeout=15.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)).content.lower() == 'yes':
    await interaction.followup.send(f"What do you want to change? 'remove' to remove an event, 'add' to add a new event.")
    change_msg = await bot.wait_for('message', timeout=15.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
    if change_msg.content.lower() == 'remove':
      await interaction.followup.send("Which event do you want to remove? Type the event name.")
      remove_event_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
      if remove_event_msg.content not in event_list:
        await interaction.followup.send("Event not found.")
        return
      event_list.remove(remove_event_msg.content)
      await interaction.followup.send(f"Event '{remove_event_msg.content}' removed.")
    elif change_msg.content.lower() == 'add':
      await interaction.followup.send("What is the name of the new event?")
      new_event_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
      event_list.append(new_event_msg.content)
      await interaction.followup.send(f"Event '{new_event_msg.content}' added.")
      while True:
        await interaction.followup.send(f"Please provide times for the new event '{new_event_msg.content}'. Type 'stop' to finish.")
        time_currentlist = []
        while True:
          try:
            time_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
            if time_msg.content.lower() == 'stop':
              if not time_currentlist:
                await interaction.followup.send("No times were provided. Cancelling event creation.")
                return
              time_list.append(time_currentlist)
              break
            await interaction.followup.send(f"Time '{time_msg.content}' added for event '{new_event_msg.content}'.")
            time_currentlist.append(time_msg.content)  # time added
          except asyncio.TimeoutError:
            await interaction.followup.send("Time input timed out. Please start again.")
            return
        break
  # create poll for the combinations
  await interaction.followup.send("Creating poll for the events and times.")

  #24 hours from now
  poll = discord.Poll("Event Poll", timedelta(hours=24))
  for event in event_list:
    for time in time_list[event_list.index(event)]:
      poll.add_answer(text=f"Event: {event} - Time: {time}")
  # poll.layout_type

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