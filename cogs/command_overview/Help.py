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

    @nextcord.slash_command(name='help', description='explanations for all command')
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def help(self,
                   interaction: nextcord.Interaction,
                   *,
                   commandname: str = nextcord.SlashOption(description="which command do you need help for", required=True, min_length=2, max_length=50)):
        """This command generates a select box that is corresponding to all commands of the bot.
           It delivers help for the usage of said commands."""

        if not commandname.startswith("/"):
            commandname = f"/{commandname}"

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /help")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if commandname not in self.client.Lists.HELP_AUTOCOMPLETE_TUPLE:
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{commandname}` isn't a valid commandname."), ephemeral=True)
            return

        HELP_OUTPUT = {**self.client.Lists.HELP_PERMISSION_OUTPUT, **self.client.Lists.HELP_NORMAL_OUTPUT}

        if len(HELP_OUTPUT[commandname]) == 3:
            permissions_text = HELP_OUTPUT[commandname][2]
        else:
            permissions_text = ""

        embed = EmbedFunctions.builder(
            color = self.client.BOT_COLOR,
            title = f"Help for `{commandname}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Syntax:",
                    "\n".join([line.strip() for line in HELP_OUTPUT[commandname][0].split("\n")]),
                    False
                ],

                [
                    "Example:",
                    HELP_OUTPUT[commandname][1],
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

        CommandUsesDB("help_selections").update(f"{commandname[1:]}")

    ####################################################################################################

    @help.on_autocomplete("commandname")
    async def autocomplete_reminder_delete(self,
                                           interaction: nextcord.Interaction,
                                           commandname: str):
        all_commands = self.client.Lists.HELP_AUTOCOMPLETE_TUPLE
        all_commands_dict = {}

        for command in all_commands:
            all_commands_dict.update({command: command[1:]})

        autocomplete_dict = Get().autocomplete_dict_from_search_string(commandname, all_commands_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(Help(client))