###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import COMMAND_LIST, BOT_COLOR
from utilities.partial_commands import embed_builder



class commandlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###commandlist###########################################################

    @nextcord.slash_command(name = "commandlist", description = "a list of all main commands")
    async def commandlist(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /commandlist")

        embed = embed_builder(title = "A list of all main commands",
                              color = BOT_COLOR,

                              field_one_name = "Commands:",
                              field_one_value = COMMAND_LIST,
                              field_one_inline = True,

                              field_two_name = "Help:",
                              field_two_value = "Explanations for singular commands can be found by typing `/help`!",
                              field_two_inline = False)
        
        await interaction.send(embed=embed, ephemeral=True)

        uses_update("command_uses", "commandlist")

    ###commandlist#alias###########################################################

    @nextcord.slash_command(name = "cl", description = "a list of all main commands (alias of /commandlist)")
    async def cl(self,
                 interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /cl")

        embed = embed_builder(title = "A list of all main commands",
                              color = BOT_COLOR,

                              field_one_name = "Commands:",
                              field_one_value = COMMAND_LIST,
                              field_one_inline = True,

                              field_two_name = "Help:",
                              field_two_value = "Explanations for singular commands can be found by typing `/help`!",
                              field_two_inline = False)
        
        await interaction.send(embed=embed, ephemeral=True)

        uses_update("command_uses", "cl")

def setup(client):
    client.add_cog(commandlist(client))