###package#import###############################################################################

import dotenv
import nextcord
import os
import pylast
import time

dotenv.load_dotenv()

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################





network = pylast.LastFMNetwork(api_key = os.getenv("LAST_FM_API_KEY"),
                               api_secret = os.getenv("LAST_FM_API_SECRET"),
                               username = os.getenv("LAST_FM_USERNAME"),
                               password_hash = pylast.md5(os.getenv("LAST_FM_PASSWORD")))

start_time = int(time.time())



class GlobalData(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    

def setup(client):
    client.add_cog(GlobalData(client))