from discord
from discord.ext import commands


# setup

BOT_TOKEN = os.environ["DISCORD_TOKEN"]
DEV_CHANNEL = 1253303598666747965 # make this settable for every server later on
intents1 = Intents.all()
intents1.members = True
bot = commands.Bot(command_prefix='!', intents=intents1)
# setup end

@bot.event
async def on_ready():
  print("bot is active")
  print(f'{bot.user} has connected to Discord!')
  dev_channel = bot.get_channel(DEV_CHANNEL)
  await dev_channel.send("BOT ACTIVE")
  synced = await bot.tree.sync()
  print("synced" + str(len(synced)))

@bot.tree.command(name="help",description="Shows all usable commands")
async def help(interaction: discord.Interaction):
  # learn about different displays
  await interaction.response.send_message("Not implemented yet")
  # retırms empty list
  # await interaction.response.send_message("Here are all the commands: " + str(all_commands))

@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
  await interaction.response.send_message("test command")

@bot.tree.command(name"shutdown", description="Shuts down the bot.")
async def close_bot(interaction: discord.Interaction):
  await interaction.response.send_message("Shutting down: " + str(bot.user))
  await bot.close()

@bot.event
async def on_disconnect():
  print("Bot is disconnected")


def main():
  bot.run(BOT_TOKEN)
main()
