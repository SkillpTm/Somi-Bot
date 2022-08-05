###package#import###############################################################################

import nextcord
from nextcord.ext import commands
import time as unix_time

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################





start_time = int(unix_time.time())



class global_data(commands.Cog):

    def __init__(self, client):
        self.client = client

    

def setup(client):
    client.add_cog(global_data(client))