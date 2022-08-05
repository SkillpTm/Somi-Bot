###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer
from utilities.variables import MODERATOR_ID, MOD_COMMANDS, BOT_COLOR



class modcommandlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###modcommandlist###########################################################

    @nextcord.slash_command(name = "modcommandlist", description = "A list of all mod commands")
    @application_checks.has_any_role(MODERATOR_ID)
    async def modcommandlist(self,
                             interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /modcommandlist")

        embed = Embed(title="A list of all mod commands",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed.add_field(name = "Commands:", value = MOD_COMMANDS, inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("mod_command_uses", "modcommandlist")

    @modcommandlist.error
    async def modcommandlist_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

    ###modcommandlist#alias###########################################################

    @nextcord.slash_command(name = "mcl", description = "A list of all mod commands (alias of /modcommandlist)")
    @application_checks.has_any_role(MODERATOR_ID)
    async def mcl(self,
                  interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /mcl")

        embed = Embed(title="A list of all mod commands",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed.add_field(name = "Commands:", value = MOD_COMMANDS, inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("mod_command_uses", "mcl")

    @mcl.error
    async def mcl_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(modcommandlist(client))