import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import YesNoButtons, SomiBot



class Shutdown(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "shutdown",
        description = "shuts the bot down",
        guild_ids = [SomiBot.SUPPORT_SERVER_ID],
        default_member_permissions=nextcord.Permissions(administrator=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks().interaction_by_owner and Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def shutdown(self, interaction: nextcord.Interaction) -> None:
        """This command let's you shutdown the bot, it can only be executed from a moderator on Somicord."""

        self.client.Loggers.action_log(Get().log_message(interaction, "/shutdown"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to shutdown the bot?", self.client), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().error("The bot has not been shutdown"), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success("The bot is being shutdown..."), ephemeral=True)


        #TODO make this support server based*
        # audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        # if audit_log_id:
        #     embed = EmbedFunctions().builder(
        #         color = nextcord.Color.orange(),
        #         author = "Mod Activity",
        #         author_icon = interaction.user.display_avatar,
        #         footer = "DEFAULT_KST_FOOTER",
        #         fields = [
        #             [
        #                 "/shutdown:",
        #                 f"{interaction.user.mention} shutdown the bot",
        #                 False
        #             ]
        #         ]
        #     )

        #     await  self.client.get_channel(audit_log_id).send(embed=embed)

        await self.client.close()



def setup(client: SomiBot) -> None:
    client.add_cog(Shutdown(client))