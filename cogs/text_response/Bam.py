####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks
from lib.utilities import SomiBot



class Bam(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "bam", description = "bams a member")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def bam(self,
                  interaction: nextcord.Interaction):
        """This command fake bans someone"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /bam")

        await interaction.response.send_message(f"User has been bammed!\n{self.client.BAN_HAMMER_GIF}")



def setup(client: SomiBot):
    client.add_cog(Bam(client))