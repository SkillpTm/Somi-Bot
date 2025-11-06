import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomCommand(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "cc",
        description = "post a custom-command",
        name_localizations = {country_tag:"custom-command" for country_tag in nextcord.Locale}
    )
    async def customcommand(
        self,
        interaction: nextcord.Interaction,
        *,
        name: str = nextcord.SlashOption(
            description = "the name of the custom-command",
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command will post a custom-command, if given it's name"""

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/custom-command",
            {"name": name}
        ))

        name = Get.clean_input_command(name)

        if not (commandtext := await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).get_text(name)):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"There is no custom-command with the name `{name}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.response.send_message(commandtext)

    ####################################################################################################

    @customcommand.on_autocomplete("name")
    async def customcommand_autocomplete_name(
        self,
        interaction: nextcord.Interaction,
        name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                name,
                {command: command for command in await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).get_list()}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(CustomCommand(client))