####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB, CustomCommandsDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomDelete(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import custom

    ####################################################################################################

    @custom.subcommand(name = "delete", description = "delete a custom-command")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def custom_delete(self,
                            interaction: nextcord.Interaction,
                            *,
                            commandname: str = nextcord.SlashOption(description="custom-command to be deleted", required=True, min_length=2, max_length=50)):
        """This command deletes a custom-command from the server's custom-commands"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /custom delete {commandname}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        commandname = Get().clean_input_command(commandname)

        commandtext = CustomCommandsDB(interaction.guild.id).delete(commandname)

        if commandtext == "":
            await interaction.followup.send(embed=EmbedFunctions().error(f"There is no custom-command with the name `{commandname}`.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"The custom-command `{commandname}` has been deleted."), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/custom delete:",
                    f"{interaction.user.mention} deleted: `{commandname}` from the custom-commands.",
                    False
                ],

                [
                    "Command text:",
                    f"`{commandtext}`",
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

    ####################################################################################################

    @custom_delete.on_autocomplete("commandname")
    async def autocomplete_commandname(self,
                                       interaction: nextcord.Interaction,
                                       commandname: str):
        all_commandnames = CustomCommandsDB(interaction.guild.id).get_list()

        all_commandnames_dict = {command: command for command in all_commandnames}

        autocomplete_dict = Get().autocomplete_dict_from_search_string(commandname, all_commandnames_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(CustomDelete(client))