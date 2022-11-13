###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import MODERATOR_ID, MOD_COMMANDS, BOT_COLOR



class ModCommandList(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###modcommandlist###########################################################

    @nextcord.slash_command(name = "mcl", description = "[MOD] a list of all mod commands", name_localizations = {country_tag:"modcommandlist" for country_tag in nextcord.Locale})
    @nextcord.ext.application_checks.has_permissions(manage_guild=True)
    async def modcommandlist(self,
                             interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /modcommandlist")

        embed = embed_builder(title = "A list of all mod commands",
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Commands:",
                              field_one_value = MOD_COMMANDS,
                              field_one_inline = False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("mod_command_uses", "modcommandlist")

    @modcommandlist.error
    async def modcommandlist_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(ModCommandList(client))