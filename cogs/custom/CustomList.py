import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.utilities import SomiBot



class CustomList(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        Commands().data["custom-list"].alias,
        Commands().data["custom-list"].description,
        name_localizations = {country_tag: Commands().data["custom-list"].name for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def custom_list(self, interaction: nextcord.Interaction) -> None:
        """This command provides a list of all custom-commands of a guild"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (all_commandnames := await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).get_list()):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("There are no custom-commands on this server.\nTo add a custom-command use `/custom add`."), ephemeral=True)
            return

        output = ""

        for commandname in all_commandnames:
            output += f"/cc `{commandname}`\n"

        if interaction.guild.icon:
            server_icon_url = interaction.guild.icon.url
        else:
            server_icon_url = Config().DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"custom-command list for {interaction.guild.name}",
            author_icon = server_icon_url,
            fields = [
                [
                    "custom-commands:",
                    output,
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomList(client))