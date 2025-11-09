import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.utilities import SomiBot, YesNoButtons



class Shutdown(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        Commands().data["shutdown"].name,
        Commands().data["shutdown"].description,
        guild_ids = [Config().SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(administrator=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Get.interaction_by_owner())
    async def shutdown(self, interaction: nextcord.Interaction) -> None:
        """This command let's you shutdown the bot, it can only be executed from a moderator on Somicord."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().get_info_message("Do you really want to shutdown the bot?"), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("The bot has not been shutdown"), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("The bot is being shutdown..."), ephemeral=True)


        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Dev Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/shutdown:",
                    f"{interaction.user.mention} shutdown the bot",
                    False
                ]
            ]
        )

        await self.client.get_channel(Config().SUPPORT_SERVER_LOGS_ID).send(embed=embed)
        await self.client.close()



def setup(client: SomiBot) -> None:
    client.add_cog(Shutdown(client))