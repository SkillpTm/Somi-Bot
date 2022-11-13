###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_kst_time_stamp



class KST(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###kst###########################################################

    @nextcord.slash_command(name = "kst", description = "shows the current time in KST")
    async def kst(self,
                  interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /kst")

        kst_timestamp = get_kst_time_stamp(source = "/kst")

        await interaction.response.send_message(kst_timestamp)

        uses_update("command_uses", "kst")



def setup(client):
    client.add_cog(KST(client))