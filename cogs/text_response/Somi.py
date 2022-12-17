####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks
from lib.utilities import SomiBot



class Somi(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "somi", description = "speaks facts")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def somi(self,
                   interaction: nextcord.Interaction):
        """This command tells you the truth"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /somi")

        await interaction.response.send_message(f"Somi best grill\n{self.client.SOMI_BEST_GRILL_IMAGE}")



def setup(client: SomiBot):
    client.add_cog(Somi(client))