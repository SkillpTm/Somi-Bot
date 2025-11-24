import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from cogs.basic.ParentCommand import ParentCommand
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Restart(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.sudo.subcommand(Commands().data["sudo restart"].name, Commands().data["sudo restart"].description)
    @nextcord_AC.check(Get.interaction_by_owner()) # type: ignore
    async def restart(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command restarts the bot, it can only be executed from a moderator on Somicord"""

        await interaction.send(embed=EmbedFunctions().get_success_message("Restarting bot..."), ephemeral=True)

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Dev Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["sudo restart"].name}:",
                    f"{interaction.user.mention} restarted the bot.",
                    True
                )
            ]
        )

        await self.client.get_channel(Config().SUPPORT_SERVER_LOGS_ID).send(embed=embed) # type: ignore
        self.client.restart()



def setup(client: SomiBot) -> None:
    client.add_cog(Restart(client))