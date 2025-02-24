####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import CommandUsesDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Help(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name='help', description='explanations for every command')
    @nextcord_AC.check(not Checks.interaction_not_by_bot)
    async def help(
        self,
        interaction: nextcord.Interaction,
        *,
        command_name: str = nextcord.SlashOption(description="which command do you need help for", required=True, min_length=2, max_length=50)
    ) -> None:
        """This command generates a select box that is corresponding to all commands of the bot.
           It delivers help for the usage of said commands."""

        # ensure /[name] syntax
        if not command_name.startswith("/"):
            command_name = f"/{command_name}"

        self.client.Loggers.action_log(Get().interaction_log_message(interaction, "/help"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        # if not a command name return early
        if command_name not in self.client.Lists.HELP_AUTOCOMPLETE_TUPLE:
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{command_name}` isn't a valid command name."), ephemeral=True)
            return

        HELP_OUTPUT = {**self.client.Lists.HELP_PERMISSION_OUTPUT, **self.client.Lists.HELP_NORMAL_OUTPUT}

        # check if the command is a permission command (permission command dicts have 3 elements, regular just 2)
        if len(HELP_OUTPUT[command_name]) == 3:
            permissions_text = HELP_OUTPUT[command_name][2]
        else:
            permissions_text = "" # an empty string will lead for the field to no be displayed

        embed = EmbedFunctions.builder(
            color = self.client.BOT_COLOR,
            title = f"Help for `{command_name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Syntax:",
                    "\n".join([line.strip() for line in HELP_OUTPUT[command_name][0].split("\n")]),
                    False
                ],

                [
                    "Example:",
                    HELP_OUTPUT[command_name][1],
                    False
                ],

                [
                    "Required Default Permissions:",
                    permissions_text,
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

        CommandUsesDB("help_selections").update(f"{command_name[1:]}")

    ####################################################################################################

    @help.on_autocomplete("command_name")
    async def autocomplete_reminder_delete(
        self,
        interaction: nextcord.Interaction,
        command_name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        all_commands = self.client.Lists.HELP_AUTOCOMPLETE_TUPLE
        all_commands_dict = {}

        for command in all_commands:
            all_commands_dict.update({command: command[1:]})

        autocomplete_dict = Get().autocomplete_dict_from_search_string(command_name, all_commands_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(Help(client))