import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Order
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot, YesNoButtons



class CustomDelete(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.custom.subcommand(Commands().data["custom delete"].name, Commands().data["custom delete"].description)
    async def custom_delete(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        name: str = nextcord.SlashOption(
            Commands().data["custom delete"].parameters["name"].name,
            Commands().data["custom delete"].parameters["name"].description,
            required = False,
            min_length = 2,
            max_length = 50
        ),
        delete_all: typing.Literal["Yes", ""] = nextcord.SlashOption(
            Commands().data["custom delete"].parameters["delete_all"].name,
            Commands().data["custom delete"].parameters["delete_all"].description,
            required = False,
            choices = ["Yes"],
            min_length = 2,
            max_length = 50,
            default = ""
        )
    ) -> None:
        """This command deletes a custom-command from the server's custom-commands"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not name and not delete_all:
            await interaction.send(embed=EmbedFunctions().get_error_message("Please either provide a custom command name or choose to delete all your custom commands."))
            return

        if delete_all == "Yes":
            await self.delete_all(interaction)
            return

        name = Get.clean_input_command(name)

        if not (commandtext := await db.CustomCommand.TEXT.get({db.CustomCommand.NAME: name, db.CustomCommand.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"There is no custom-command with the name `{name}`.\nTo get a list of the custom-commands use `/custom-list`."))
            return

        await db.CustomCommand._.delete(where={db.CustomCommand.NAME: name, db.CustomCommand.SERVER: interaction.guild.id})
        await interaction.send(embed=EmbedFunctions().get_success_message(f"The custom-command `{name}` has been deleted."))


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["custom delete"].full_name}:s",
                    f"{interaction.user.mention} deleted: `{name}` from the custom-commands.",
                    False
                ),
                EmbedField(
                    "Command text:",
                    f"`{commandtext}`",
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    async def delete_all(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """asks the user if they want to delete all their custom commands and does as answered"""

        if not await db.CustomCommand._.get_all(where={db.CustomCommand.SERVER: interaction.guild.id}):
            await interaction.send(embed=EmbedFunctions().get_error_message("There are no custom-commands to delete, on this server."))
            return

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to delete **ALL** your custom commands __**(they can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("Your custom commands have **not** been deleted!"), ephemeral=True)
            return

        await db.CustomCommand._.delete(where={db.CustomCommand.SERVER: interaction.guild.id}, limit=1_000_000)
        await interaction.send(embed=EmbedFunctions().get_success_message("**ALL** your custom commands have been deleted!"), ephemeral=True)


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["custom delete"].full_name}:",
                    f"{interaction.user.mention} deleted: all the custom-commands.",
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    @custom_delete.on_autocomplete("name")
    async def custom_delete_autocomplete_name(
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
    client.add_cog(CustomDelete(client))