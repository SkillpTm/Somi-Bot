import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Help(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["help"].name,
        Commands().data["help"].description,
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def help(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        name: str = nextcord.SlashOption(
            Commands().data["help"].parameters["name"].name,
            Commands().data["help"].parameters["name"].description,
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command generates a select box that is corresponding to all commands of the bot.
           It delivers help for the usage of said commands."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        name = name[1:] if name.startswith("/") else name

        if name not in Commands().overview.values():
            await interaction.send(embed=EmbedFunctions().get_error_message(f"`{name}` isn't a valid command name."))
            return

        parent_alias = Commands().data[name].parent.alias or Commands().data[name].parent.name
        sub_alias = Commands().data[name].alias or Commands().data[name].name
        alias = f"{parent_alias} {sub_alias}".strip()
        if alias != Commands().data[name].full_name:
            alias_line = f"`Alias:` /{alias}\n"
        else:
            alias_line = ""

        if Commands().data[name].permissions:
            permission_line = "\nRequired Permissions:\n" + "".join([f"- {permission} :white_check_mark:\n" for permission in Commands().data[name].permissions])
        else:
            permission_line = ""

        parameter_fields: list[EmbedField] = []

        for parameter in Commands().data[name].parameters.values():
            parameter_fields.append(EmbedField(
                f"`{parameter.name}` - ({'required' if parameter.required else 'optional'})",
                f"{parameter.description}\n`Type:` {parameter.type}\n{'`Default:` ' + parameter.default if parameter.default else ''}",
                False
            ))

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            title = f"Help for `/{Commands().data[name].full_name}`",
            description = f"{Commands().data[name].description}\n" + alias_line + permission_line,
            footer = f"Example: {Commands().data[name].example}",
            fields = [
                EmbedField(
                    "Structure:",
                    f"```{Commands().data[name].structure}```",
                    False
                ),
                *parameter_fields
            ]
        )

        await interaction.send(embed=embed)
        await db.Telemetry.AMOUNT.increment(f"help selection: {name[1:]}")


    @help.on_autocomplete("name")
    async def help_autocomplete_name(
        self,
        interaction: nextcord.Interaction[SomiBot],
        name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                name,
                Commands().overview
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Help(client))