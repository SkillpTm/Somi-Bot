###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import BAN_HAMMER_GIF



class Bam(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###bam###########################################################

    @nextcord.slash_command(name = "bam", description = "bams a user")
    async def bam(self,
                  interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /bam")

        await interaction.response.send_message(f"User has been bammed!\n{BAN_HAMMER_GIF}")

        uses_update("command_uses", "bam")



def setup(client):
    client.add_cog(Bam(client))