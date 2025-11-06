import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Help(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="help", description="explanations for every command")
    async def help(
        self,
        interaction: nextcord.Interaction,
        *,
        name: str = nextcord.SlashOption(
            description = "which command do you need help for",
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command generates a select box that is corresponding to all commands of the bot.
           It delivers help for the usage of said commands."""

        # ensure /[name] syntax
        if not name.startswith("/"):
            name = f"/{name}"

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/help",
            {"name": name}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if name not in self.client.lists.HELP_AUTOCOMPLETE_TUPLE:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"`{name}` isn't a valid command name."), ephemeral=True)
            return

        help_oputput = {**self.client.lists.HELP_PERMISSION_OUTPUT, **self.client.lists.HELP_NORMAL_OUTPUT}

        embed = EmbedFunctions.builder(
            color = self.client.config.BOT_COLOR,
            title = f"Help for `{name}`",
            fields = [
                [
                    "Syntax:",
                    "\n".join([line.strip() for line in help_oputput[name][0].split("\n")]),
                    False
                ],

                [
                    "Example:",
                    help_oputput[name][1],
                    False
                ],

                [
                    "Required Default Permissions:",
                    help_oputput[name][2] if len(help_oputput[name]) == 3 else "",
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

        await (await DBHandler(self.client.database).telemetry()).increment(f"help selection: {name[1:]}")

    ####################################################################################################

    @help.on_autocomplete("name")
    async def help_autocomplete_name(
        self,
        interaction: nextcord.Interaction,
        name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                name,
                {command: command[1:] for command in self.client.lists.HELP_AUTOCOMPLETE_TUPLE}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Help(client))