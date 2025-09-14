import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import Get
from lib.utilities import SomiBot



class KST(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="kst", description="shows the current time in KST")
    async def kst(self, interaction: nextcord.Interaction) -> None:
        """This command will display the current date and time in KST"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/kst"))

        await interaction.response.send_message(Get.kst_timestamp(True))



def setup(client: SomiBot) -> None:
    client.add_cog(KST(client))