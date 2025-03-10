import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.dbModules import DBHandler
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Help(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "help", description = "explanations for every command")
    @nextcord_AC.check(Checks.interaction_not_by_bot())
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

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/help",
            {"name": name}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        # if not a command name return early
        if name not in self.client.Lists.HELP_AUTOCOMPLETE_TUPLE:
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{name}` isn't a valid command name."), ephemeral=True)
            return

        HELP_OUTPUT = {**self.client.Lists.HELP_PERMISSION_OUTPUT, **self.client.Lists.HELP_NORMAL_OUTPUT}

        # check if the command is a permission command (permission command dicts have 3 elements, regular just 2)
        if len(HELP_OUTPUT[name]) == 3:
            permissions_text = HELP_OUTPUT[name][2]
        else:
            permissions_text = "" # an empty string will lead for the field to no be displayed

        embed = EmbedFunctions.builder(
            color = self.client.BOT_COLOR,
            title = f"Help for `{name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Syntax:",
                    "\n".join([line.strip() for line in HELP_OUTPUT[name][0].split("\n")]),
                    False
                ],

                [
                    "Example:",
                    HELP_OUTPUT[name][1],
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

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment(f"help selection: {name[1:]}")

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
                {command: command[1:] for command in self.client.Lists.HELP_AUTOCOMPLETE_TUPLE}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Help(client))