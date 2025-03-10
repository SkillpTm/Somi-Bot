import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import re

from lib.dbModules import DBHandler
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class CustomAdd(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import custom

    ####################################################################################################

    @custom.subcommand(name = "add", description = "add a custom-command to this server")
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def custom_add(
        self,
        interaction: nextcord.Interaction,
        *,
        name: str = nextcord.SlashOption(
            description = "new custom-command name",
            required = True,
            min_length = 2,
            max_length = 50
        ),
        text: str = nextcord.SlashOption(
            description = "the content of the new custom-command",
            required = True,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command adds a custom-command to the server's custom-commands"""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/custom add",
            {"name": name, "text": text}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        name = Get.clean_input_command(name)

        # make sure name is only letters and numbers
        if not re.match(r"^[\da-z]+$", name):
            await interaction.followup.send(embed=EmbedFunctions().error("You can only have letters and numbers in your custom-name!"), ephemeral=True)
            return

        added = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).custom_command()).add(name, text)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error(f"A custom-command with the name `{name}` already exists.\nTo get a list of the custom-commands use `/custom-list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"Your custom-command with the name `{name}` has been created."), ephemeral=True)


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
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

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomAdd(client))