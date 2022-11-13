###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import SOMI_BEST_GRILL_IMAGE



class Somi(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###somi###########################################################

    @nextcord.slash_command(name = "somi", description = "speaks facts")
    async def somi(self,
                   interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /somi")

        await interaction.response.send_message(f"Somi best grill\n{SOMI_BEST_GRILL_IMAGE}")

        uses_update("command_uses", "somi")



def setup(client):
    client.add_cog(Somi(client))