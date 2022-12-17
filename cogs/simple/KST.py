####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks, Get
from lib.utilities import SomiBot



class KST(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "kst", description = "shows the current time in KST")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def kst(self,
                  interaction: nextcord.Interaction):
        """This command will display the current date and time in KST"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /kst")

        await interaction.response.send_message(Get().kst_timestamp(source = "/kst"))



def setup(client: SomiBot):
    client.add_cog(KST(client))