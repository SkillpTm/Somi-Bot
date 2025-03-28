import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomList(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "cl",
        description = "a list of all custom-commands on this server",
        name_localizations = {country_tag:"custom-list" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def custom_list(self, interaction: nextcord.Interaction) -> None:
        """This command provides a list of all custom-commands of a guild"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/custom list"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        all_commandnames = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).custom_command()).get_list()

        if not all_commandnames:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("There are no custom-commands on this server.\nTo add a custom-command use `/custom add`."), ephemeral=True)
            return

        output = ""

        # formatting the output
        for commandname in all_commandnames:
            output += f"/cc `{commandname}`\n"

        if interaction.guild.icon:
            server_icon_url = interaction.guild.icon.url
        else:
            server_icon_url = self.client.DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"custom-command list for {interaction.guild.name}",
            author_icon = server_icon_url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "custom-commands:",
                    output[:1000],
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomList(client))