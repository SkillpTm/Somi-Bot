import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Bam(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(Commands().data["bam"].name, Commands().data["avatar"].description)
    async def bam(self, interaction: nextcord.Interaction) -> None:
        """This command fake bans someone"""

        await interaction.response.send_message(f"User has been bammed!\n{Config().BAN_HAMMER_GIF}")



def setup(client: SomiBot) -> None:
    client.add_cog(Bam(client))