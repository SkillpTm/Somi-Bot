import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomDelete(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.custom.subcommand(name="delete", description="delete a custom-command")
    async def custom_delete(
        self,
        interaction: nextcord.Interaction,
        *,
        name: str = nextcord.SlashOption(
            description = "custom-command to be deleted",
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command deletes a custom-command from the server's custom-commands"""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/custom delete",
            {"name": name}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        name = Get.clean_input_command(name)

        commandtext = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).custom_command()).delete(name)

        if not commandtext:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"There is no custom-command with the name `{name}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"The custom-command `{name}` has been deleted."), ephemeral=True)


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
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

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

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
                {command: command for command in await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).custom_command()).get_list()}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(CustomDelete(client))