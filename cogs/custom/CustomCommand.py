import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import CustomCommandsDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomCommand(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "cc", description = "post a custom-command", name_localizations = {country_tag:"custom-command" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def customcommand(
        self,
        interaction: nextcord.Interaction,
        *,
        commandname: str = nextcord.SlashOption(
            description = "the name of the custom-command",
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command will post a custom-command, if given it's name"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/custom-command",
            {"commandname": commandname}
        ))

        commandname = Get().clean_input_command(commandname)

        commandtext = CustomCommandsDB(interaction.guild.id).get_text(commandname)

        if not commandtext:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"There is no custom-command with the name `{commandname}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.response.send_message(commandtext)

    ####################################################################################################

    @customcommand.on_autocomplete("commandname")
    async def autocomplete_commandname(
        self,
        interaction: nextcord.Interaction,
        commandname: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        all_commandnames = CustomCommandsDB(interaction.guild.id).get_list()
        all_commandnames_dict = {command: command for command in all_commandnames}
        autocomplete_dict = Get().autocomplete_dict_from_search_string(commandname, all_commandnames_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomCommand(client))