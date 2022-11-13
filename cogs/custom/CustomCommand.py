###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import list_custom, command_custom
from utilities.maincommands import checks
from utilities.partial_commands import make_input_command_clean, string_search_to_list



class CustomCommand(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###customcommand###########################################################

    @nextcord.slash_command(name='cc', description="post a custom command", name_localizations = {country_tag:"customcommand" for country_tag in nextcord.Locale})
    async def customcommand(self,
                            interaction: nextcord.Interaction,
                            *,
                            commandname: str = nextcord.SlashOption(description="the name of the custom command", required=True, min_length=2, max_length=32)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /customcommand {commandname}")

        clean_commandname = make_input_command_clean(commandname)

        commandtext = command_custom(interaction.guild.id, clean_commandname)

        if commandtext == "":
            await interaction.response.send_message(f"There is no custom command with the name `{clean_commandname}`.", ephemeral=True)
            return

        await interaction.response.send_message(commandtext)

        uses_update("command_uses", "customcommand")
        uses_update("custom_command_uses", f"{clean_commandname}")

    @customcommand.on_autocomplete("commandname")
    async def autocomplete_commandname(self,
                                       interaction: nextcord.Interaction,
                                       commandname: str):
        all_commandnames = list_custom(interaction.guild.id)

        autocomplete_list = string_search_to_list(commandname, all_commandnames)

        await interaction.response.send_autocomplete(autocomplete_list)



def setup(client):
    client.add_cog(CustomCommand(client))