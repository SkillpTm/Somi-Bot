import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Invite(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["invite"].name,
        Commands().data["invite"].description,
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
    async def invite(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command posts the invite link for the bot"""

        await interaction.send(f"<{Config().BOT_INVITE}>")



def setup(client: SomiBot) -> None:
    client.add_cog(Invite(client))