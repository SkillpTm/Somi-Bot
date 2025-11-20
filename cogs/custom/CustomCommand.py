import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db, Order
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot



class CustomCommand(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["custom-command"].alias,
        Commands().data["custom-command"].description,
        name_localizations = {country_tag: Commands().data["custom-command"].name for country_tag in nextcord.Locale}
    )
    async def customcommand(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        name: str = nextcord.SlashOption(
            Commands().data["custom-command"].parameters["name"].name,
            Commands().data["custom-command"].parameters["name"].description,
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command will post a custom-command, if given it's name"""

        name = Get.clean_input_command(name)

        if not (commandtext := await db.CustomCommand.TEXT.get({db.CustomCommand.NAME: name, db.CustomCommand.SERVER: interaction.guild.id})):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"There is no custom-command with the name `{name}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.response.send_message(commandtext)


    @customcommand.on_autocomplete("name")
    async def customcommand_autocomplete_name(
        self,
        interaction: nextcord.Interaction[SomiBot],
        name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        commands = {}

        async for entry in db.CustomCommand._.get_multiple(where={db.CustomCommand.SERVER: interaction.guild.id}, order_by=db.CustomCommand.NAME, order=Order.ASCENDING):
            commands.update({f"{db.CustomCommand.NAME.retrieve(entry)}: {db.CustomCommand.TEXT.retrieve(entry)}" : db.CustomCommand.NAME.retrieve(entry)})

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                name,
                commands
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(CustomCommand(client))