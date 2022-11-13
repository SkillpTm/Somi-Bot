###package#import###############################################################################

import nextcord
from nextcord.ext import commands
import os
import pylast
import time as unix_time
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################





network = pylast.LastFMNetwork(api_key = os.getenv("LAST_FM_API_KEY"),
                               api_secret = os.getenv("LAST_FM_API_SECRET"),
                               username = os.getenv("LAST_FM_USERNAME"),
                               password_hash = pylast.md5(os.getenv("LAST_FM_PASSWORD")))

start_time = int(unix_time.time())



class global_data(commands.Cog):

    def __init__(self, client):
        self.client = client

    

def setup(client):
    client.add_cog(global_data(client))