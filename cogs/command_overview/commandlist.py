###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import COMMAND_LIST, BOT_COLOR
from utilities.partial_commands import embed_kst_footer



class commandlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###commandlist###########################################################

    @nextcord.slash_command(name = "commandlist", description = "A list of all main commands")
    async def commandlist(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /commandlist")

        embed = Embed(title="A list of all main commands",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed.add_field(name = "Commands:", value = COMMAND_LIST, inline = True)
        embed.add_field(name = "Help:", value = "Explanations for singular commands can be found by typing `/help`", inline = False)
        
        await interaction.send(embed=embed, ephemeral=True)

        uses_update("command_uses", "commandlist")

    ###commandlist#alias###########################################################

    @nextcord.slash_command(name = "cl", description = "A list of all main commands (alias of /commandlist)")
    async def cl(self,
                 interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /cl")

        embed = Embed(title="A list of all main commands",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed.add_field(name = "Commands:", value = COMMAND_LIST, inline = True)
        embed.add_field(name = "Help:", value = "Explanations for singular commands can be found by typing `/help`", inline = False)
        
        await interaction.send(embed=embed, ephemeral=True)

        uses_update("command_uses", "cl")

def setup(client):
    client.add_cog(commandlist(client))