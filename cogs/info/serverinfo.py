###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_server_icon, embed_get_serverinfo
from utilities.variables import BOT_COLOR



class severinfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###serverinfo###########################################################
        
    @nextcord.slash_command(name="serverinfo", description = "gives information about this server")
    async def serverinfo(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /serverinfo")

        embed = Embed(title= f"Server Information: `{interaction.guild}`",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_server_icon(interaction, embed)
        embed_get_serverinfo(interaction, embed)

        await interaction.send(embed=embed)

        uses_update("command_uses", "serverinfo")

    ###serverinfo#alias###########################################################

    @nextcord.slash_command(name="si", description = "gives information about this server (alias of /serverinfo)")
    async def si(self,
                 interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /si")

        embed = Embed(title= f"Server Information: `{interaction.guild}`",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_server_icon(interaction, embed)
        embed_get_serverinfo(interaction, embed)

        await interaction.send(embed=embed)

        uses_update("command_uses", "si")

def setup(client):
    client.add_cog(severinfo(client))