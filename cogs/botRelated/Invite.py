import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import Get
from lib.utilities import SomiBot



class Invite(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "invite", description = "posts the bot's invite link")
    async def invite(self, interaction: nextcord.Interaction) -> None:
        """This command posts the invite link for the bot"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/about"))

        await interaction.response.send_message(f"<{self.client.SOMI_INVITE}>")



def setup(client: SomiBot) -> None:
    client.add_cog(Invite(client))