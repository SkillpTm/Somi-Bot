####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import CustomDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomCommand(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "cc", description = "post a custom-command", name_localizations = {country_tag:"custom-command" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def customcommand(self,
                            interaction: nextcord.Interaction,
                            *,
                            commandname: str = nextcord.SlashOption(description="the name of the custom-command", required=True, min_length=2, max_length=50)):
        """This command will post a custom-command, if given it's name"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /customcommand {commandname}")

        clean_commandname = Get().clean_input_command(commandname)

        commandtext = CustomDB().get_command_text(interaction.guild.id, clean_commandname)

        if commandtext == "":
            await interaction.response.send_message(embed=EmbedFunctions().error(f"There is no custom-command with the name `{clean_commandname}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.response.send_message(commandtext.replace("‘", "'"))

    @customcommand.on_autocomplete("commandname")
    async def autocomplete_commandname(self,
                                       interaction: nextcord.Interaction,
                                       commandname: str):
        all_commandnames = CustomDB().list(interaction.guild.id)

        all_commandnames_dict = {command: command for command in all_commandnames}

        autocomplete_dict = Get().autocomplete_dict_from_search_string(commandname, all_commandnames_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(CustomCommand(client))