###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import BAN_HAMMER_GIF



class bam(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###bam###########################################################

    @nextcord.slash_command(name = "bam", description = "bams a user")
    async def bam(self,
                  interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /bam")

        await interaction.response.send_message(f"User has been bammed!\n{BAN_HAMMER_GIF}")

        uses_update("command_uses", "bam")

def setup(client):
    client.add_cog(bam(client))