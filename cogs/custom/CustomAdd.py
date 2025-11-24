import re

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class CustomAdd(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.custom.subcommand(Commands().data["custom add"].name, Commands().data["custom add"].description)
    async def custom_add(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        name: str = nextcord.SlashOption(
            Commands().data["custom add"].parameters["name"].name,
            Commands().data["custom add"].parameters["name"].description,
            required = True,
            min_length = 2,
            max_length = 50
        ),
        text: str = nextcord.SlashOption(
            Commands().data["custom add"].parameters["text"].name,
            Commands().data["custom add"].parameters["text"].description,
            required = True,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command adds a custom-command to the server's custom-commands"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        name = Get.clean_input_command(name)

        # make sure name is only letters and numbers
        if not re.match(r"^[a-z0-9]+$", name):
            await interaction.send(embed=EmbedFunctions().get_error_message("You can only have letters and numbers in your custom-name!"))
            return

        if not await db.CustomCommand._.add({db.CustomCommand.NAME: name, db.CustomCommand.TEXT: text, db.CustomCommand.SERVER: interaction.guild.id}):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"A custom-command with the name `{name}` already exists.\nTo get a list of the custom-commands use `/custom-list`."))
            return

        await interaction.send(embed=EmbedFunctions().get_success_message(f"Your custom-command with the name `{name}` has been created."))


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["custom add"].name}:",
                    f"{interaction.user.mention} added: `{name}` as a custom-command.",
                    False
                ),
                EmbedField(
                    "Command text:",
                    f"`{text}`",
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(CustomAdd(client))