import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import re

from lib.db_modules import ConfigDB, CustomCommandsDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomAdd(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import custom

    ####################################################################################################

    @custom.subcommand(name = "add", description = "add a custom-command to this server")
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def custom_add(
        self,
        interaction: nextcord.Interaction,
        *,
        commandname: str = nextcord.SlashOption(
            description = "new custom-command name",
            required = True,
            min_length = 2,
            max_length = 50
        ),
        commandtext: str = nextcord.SlashOption(
            description = "the content of the new custom-command",
            required = True,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command adds a custom-command to the server's custom-commands"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/custom add",
            {"commandname": commandname, "commandtext": commandtext}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        commandname = Get().clean_input_command(commandname)

        # make sure commandname is only letters and numbers
        if not re.match(r"^[\da-z]+$", commandname):
            await interaction.followup.send(embed=EmbedFunctions().error("You can only have letters and numbers in your custom-commandname!"), ephemeral=True)
            return

        added = CustomCommandsDB(interaction.guild.id).add(commandname, commandtext)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error(f"A custom-command with the name `{commandname}` already exists.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"Your custom-command with the name `{commandname}` has been created."), ephemeral=True)


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
                    "/custom add:",
                    f"{interaction.user.mention} added: `{commandname}` as a custom-command.",
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



def setup(client: SomiBot) -> None:
    client.add_cog(CustomAdd(client))