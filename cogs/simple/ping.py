###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

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
        if not checks(interaction):
            return

        print(f"{interaction.user}: /ping")

        await interaction.response.send_message(f"ping = {round(self.client.latency * 1000)}ms\nuptime = <t:{start_time}:R>")

        uses_update("command_uses", "ping")

def setup(client):
    client.add_cog(ping(client))