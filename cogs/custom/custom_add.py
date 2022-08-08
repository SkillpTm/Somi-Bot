###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import create_custom_command
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR
from utilities.partial_commands import get_user_avatar, restart_bot, make_input_command_clean, embed_builder



class custom_add(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import custom

    ###custom#add###########################################################

    @custom.subcommand(name = "add", description = "add a custom command")
    @application_checks.has_any_role(MODERATOR_ID)
    async def custom_add(self,
                         interaction: Interaction,
                         *,
                         commandname: str = SlashOption(description="new custom command name", required=True, min_length=2, max_length=32),
                         commandtext: str = SlashOption(description="The content of the new custom command", required=True, min_length=2, max_length=1000)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /custom add {commandname}\n{commandtext}")

        clean_commandname = make_input_command_clean(commandname)

        added = create_custom_command(interaction.guild.id, clean_commandname, commandtext)

        if not added:
            await interaction.response.send_message(f"A custom command with the name `{clean_commandname}` already exists. Please select a different name.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your custom command with the name `{clean_commandname}` has been created.", ephemeral=True)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = MOD_COLOR,
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "/custom add:",
                              field_one_value = f"{interaction.user.mention} added: `{clean_commandname}` as a custom command",
                              field_one_inline = False,

                              field_two_name = "Command text:",
                              field_two_value = commandtext,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "custom add")

        restart_bot()

    @custom_add.error
    async def ban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(custom_add(client))