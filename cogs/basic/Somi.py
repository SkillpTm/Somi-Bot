import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Somi(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    @nextcord.slash_command(Commands().data["somi"].name, Commands().data["somi"].description)
    async def somi(self,interaction: nextcord.Interaction) -> None:
        """This command tells you the truth"""

        await interaction.response.send_message(f"Somi best grill!\n{Config().SOMI_BEST_GRILL_IMAGE}")



def setup(client: SomiBot) -> None:
    client.add_cog(Somi(client))