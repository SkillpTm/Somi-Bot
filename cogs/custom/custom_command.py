###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import command_custom, get_description_custom_command_names
from utilities.maincommands import checks
from utilities.partial_commands import make_input_command_clean
from utilities.variables import SERVER_ID



description_commands = get_description_custom_command_names(SERVER_ID)

class custom_command(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###customcommand###########################################################

    @nextcord.slash_command(name='customcommand', description="post a custom command")
    async def customcommand(self,
                            interaction: Interaction,
                            *,
                            commandname: str = SlashOption(description=description_commands, required=True, min_length=2, max_length=32)):
        if not checks(interaction):
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

    ###customcommand#alias###########################################################

    @nextcord.slash_command(name='cc', description="post a custom command (alias of /customcommand)")
    async def cc(self,
                 interaction: Interaction,
                 *,
                 commandname: str = SlashOption(description=description_commands, required=True, min_length=2, max_length=32)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /cc {commandname}")

        clean_commandname = make_input_command_clean(commandname)

        commandtext = command_custom(interaction.guild.id, clean_commandname)

        if commandtext == "":
            await interaction.response.send_message(f"There is no custom command with the name `{clean_commandname}`.", ephemeral=True)
            return

        await interaction.response.send_message(commandtext)

        uses_update("command_uses", "cc")
        uses_update("custom_command_uses", f"{clean_commandname}")

def setup(client):
    client.add_cog(custom_command(client))