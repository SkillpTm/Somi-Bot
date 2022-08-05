###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import SOMI_BEST_GRILL_IMAGE



class somi(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###somi###########################################################

    @nextcord.slash_command(name = "somi", description = "speaks facts")
    async def somi(self,
                   interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /somi")

        await interaction.response.send_message(f"Somi best grill\n{SOMI_BEST_GRILL_IMAGE}")

        uses_update("command_uses", "somi")

def setup(client):
    client.add_cog(somi(client))