###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from time import time

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import start_time
from database.database_command_uses import uses_update
from utilities.maincommands import checks



class ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###ping###########################################################

    @nextcord.slash_command(name = "ping", description = "shows the bot's ping")
    async def ping(self,
                   interaction: Interaction):
        start = time()
        if not checks(interaction):
            return

        print(f"{interaction.user}: /ping")

        message = await interaction.response.send_message(f"ping = `{self.client.latency * 1000:,.0f}ms`\nuptime = <t:{start_time}:R>\nVisible Users: `{len(self.client.users)}`")

        end = time()
        
        await message.edit(f"DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`\nResponse time: `{(end-start) * 1000 :,.0f}ms`\nUptime = <t:{start_time}:R>\nVisible Users: `{len(self.client.users)}`")

        uses_update("command_uses", "ping")

def setup(client):
    client.add_cog(ping(client))