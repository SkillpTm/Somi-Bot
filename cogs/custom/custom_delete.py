###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import delete_custom_command
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, restart_bot, make_input_command_clean



class custom_delete(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import custom

    ###custom#delete###########################################################

    @custom.subcommand(name = "delete", description = "delete a custom command")
    @application_checks.has_any_role(MODERATOR_ID)
    async def custom_delete(self,
                            interaction: Interaction,
                            *,
                            commandname: str = SlashOption(description="custom command to be deleted", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /custom delete {commandname}")

        clean_commandname = make_input_command_clean(commandname)

        deleted, commandtext= delete_custom_command(interaction.guild.id, clean_commandname)

        if not deleted:
            await interaction.response.send_message(f"There is no custom command with the name `{clean_commandname}`", ephemeral=True)
            return

        await interaction.response.send_message(f"The custom command `{clean_commandname}` has been removed", ephemeral=True)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        embed = Embed(colour=MOD_COLOR)
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/custom delete:", value = f"{interaction.user.mention} deleted: `{clean_commandname}` from the custom commands", inline = False)
        embed.add_field(name = "Command text:", value = commandtext, inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "custom delete")

        restart_bot()

    @custom_delete.error
    async def ban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(custom_delete(client))