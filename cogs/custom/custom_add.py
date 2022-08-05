###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import create_custom_command
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, restart_bot, make_input_command_clean



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
                         commandname: str = SlashOption(description="new custom command name", required=True),
                         commandtext: str = SlashOption(description="The content of the new custom command", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /custom add {commandname}\n{commandtext}")

        clean_commandname = make_input_command_clean(commandname)

        if len(clean_commandname) > 31:
            await interaction.response.send_message("Your custom command name needs to be smaller than 32 characters!", ephemeral=True)
            return

        if len(commandtext) > 799:
            await interaction.response.send_message("Your `commandtext` needs to be smaller than 800 characters!", ephemeral=True)
            return

        added = create_custom_command(interaction.guild.id, clean_commandname, commandtext)

        if not added:
            await interaction.response.send_message(f"A custom command with the name `{clean_commandname}` already exists. Please select a different name.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your custom command with the name `{clean_commandname}` has been created.", ephemeral=True)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        embed = Embed(colour=MOD_COLOR)
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/custom add:", value = f"{interaction.user.mention} added: `{clean_commandname}` as a custom command", inline = False)
        embed.add_field(name = "Command text:", value = commandtext, inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "custom add")

        restart_bot()

    @custom_add.error
    async def ban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(custom_add(client))