import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
# from responses import get_response

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = os.environ['DISCORD_TOKEN']

# need to set intents
intents: Intents = Intents.all()
intents.message_content = True
client: Client = Client(intents=intents)
# client = Client()

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

client.run(TOKEN)