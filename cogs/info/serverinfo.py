###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_serverinfo_embed
from utilities.variables import BOT_COLOR



class severinfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###serverinfo###########################################################
        
    @nextcord.slash_command(name="serverinfo", description = "gives information about this server")
    async def serverinfo(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /serverinfo")

        embed = await get_serverinfo_embed(self.client, interaction)

        await interaction.send(embed=embed)

        uses_update("command_uses", "serverinfo")

    ###serverinfo#alias###########################################################

    @nextcord.slash_command(name="si", description = "gives information about this server (alias of /serverinfo)")
    async def si(self,
                 interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /si")

        embed = await get_serverinfo_embed(self.client, interaction)

        await interaction.send(embed=embed)

        uses_update("command_uses", "si")

def setup(client):
    client.add_cog(severinfo(client))