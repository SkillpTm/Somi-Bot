###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import list_custom
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_server_icon_author
from utilities.variables import BOT_COLOR



class custom_list(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import custom

    ###custom#list###########################################################

    @custom.subcommand(name = "list", description = "A list of all custom commands")
    async def custom_list(self,
                          interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /custom list")

        amount, all_commandnames = list_custom(interaction.guild.id)

        if amount == 0:
            await interaction.response.send_message("There are no custom commands on this server.", ephemeral=True)

            uses_update("command_uses", "custom list")

            return

        output = ""
        i = 0

        embed = Embed(colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_server_icon_author(interaction, embed)

        while i < amount:
            output += f"/cc `{all_commandnames[i]}`\n"
            i += 1
        embed.add_field(name = "Custom commands:", value = output, inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "custom list")

def setup(client):
    client.add_cog(custom_list(client))