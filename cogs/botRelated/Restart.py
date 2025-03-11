import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Restart(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "restart",
        description = "restarts the entire bot",
        guild_ids = [SomiBot.SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(administrator=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_by_owner() and Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def restart(self, interaction: nextcord.Interaction) -> None:
        """This command restarts the bot, it can only be executed from a moderator on Somicord"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/restart"))

        await interaction.response.send_message(embed=EmbedFunctions().success("Restarting bot..."), ephemeral=True)


        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Dev Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/restart:",
                    f"{interaction.user.mention} restarted the bot.",
                    True
                ]
            ]
        )

        await self.client.get_channel(self.client.SUPPORT_SERVER_LOGS_ID).send(embed=embed)
        self.client.restart()



def setup(client: SomiBot) -> None:
    client.add_cog(Restart(client))