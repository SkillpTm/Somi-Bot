import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Invite(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(Commands().data["invite"].name, Commands().data["invite"].description)
    async def invite(self, interaction: nextcord.Interaction) -> None:
        """This command posts the invite link for the bot"""

        await interaction.response.send_message(f"<{Config().BOT_INVITE}>")



def setup(client: SomiBot) -> None:
    client.add_cog(Invite(client))