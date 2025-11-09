import re

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class CustomAdd(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.custom.subcommand(Commands().data["custom add"].name, Commands().data["custom add"].description)
    async def custom_add(
        self,
        interaction: nextcord.Interaction,
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
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only have letters and numbers in your custom-name!"), ephemeral=True)
            return

        if not await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).add(name, text):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"A custom-command with the name `{name}` already exists.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Your custom-command with the name `{name}` has been created."), ephemeral=True)


        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/custom add:",
                    f"{interaction.user.mention} added: `{name}` as a custom-command.",
                    False
                ],

                [
                    "Command text:",
                    f"`{text}`",
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomAdd(client))