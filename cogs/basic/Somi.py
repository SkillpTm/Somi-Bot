import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Somi(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["somi"].name,
        Commands().data["somi"].description,
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def somi(self,interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command tells you the truth"""

        await interaction.response.send_message(f"Somi best grill!\n{Config().SOMI_BEST_GRILL_IMAGE}")



def setup(client: SomiBot) -> None:
    client.add_cog(Somi(client))