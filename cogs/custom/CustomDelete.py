import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.utilities import SomiBot



class CustomDelete(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.custom.subcommand(Commands().data["custom delete"].name, Commands().data["custom delete"].description)
    async def custom_delete(
        self,
        interaction: nextcord.Interaction,
        *,
        name: str = nextcord.SlashOption(
            Commands().data["custom delete"].parameters["name"].name,
            Commands().data["custom delete"].parameters["name"].description,
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command deletes a custom-command from the server's custom-commands"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        name = Get.clean_input_command(name)

        if not (commandtext := await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).delete(name)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"There is no custom-command with the name `{name}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"The custom-command `{name}` has been deleted."), ephemeral=True)


        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/custom delete:",
                    f"{interaction.user.mention} deleted: `{name}` from the custom-commands.",
                    False
                ],

                [
                    "Command text:",
                    f"`{commandtext}`",
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

    ####################################################################################################

    @custom_delete.on_autocomplete("name")
    async def custom_delete_autocomplete_name(
        self,
        interaction: nextcord.Interaction,
        name: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                name,
                {command: command for command in await (await DBHandler(self.client.database, server_id=interaction.guild.id).custom_command()).get_list()}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(CustomDelete(client))