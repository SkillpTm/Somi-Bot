####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks
from lib.utilities import SomiBot



class Invite(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "invite", description = "posts the bot's invite link")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def invite(self,
                     interaction: nextcord.Interaction):
        """This command posts the invite link for the bot"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /invite")

        await interaction.response.send_message(f"<{self.client.SOMI_INVITE}>")



def setup(client: SomiBot):
    client.add_cog(Invite(client))