###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import HELP_OPTIONS, HELP_OUTPUT, BOT_COLOR
from utilities.partial_commands import embed_builder

class HelpDropdownView(nextcord.ui.View):
    @nextcord.ui.select(placeholder = "Select a command", min_values=1, max_values=1, options = HELP_OPTIONS)

    async def callback(self,
                       select,
                       interaction):
        selection = select.values[0]

        print(f"{interaction.user}: /help {selection}")

        embed = embed_builder(title = f"Help for /{selection}",
                              color = BOT_COLOR,

                              field_one_name = "Syntax:",
                              field_one_value = HELP_OUTPUT[selection][0],
                              field_one_inline = False,

                              field_two_name = "Info:",
                              field_two_value = HELP_OUTPUT[selection][1],
                              field_two_inline = False)

        await interaction.edit(content=None, embed=embed)

        uses_update("help_selections", f"{selection}")



class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###help###########################################################

    @nextcord.slash_command(name='help', description='Explanations for all command')
    async def help(self,
                   interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /help")

        HelpDropView = HelpDropdownView()
        await interaction.response.send_message("What command do you need help with?", view=HelpDropView, ephemeral=True)

        uses_update("command_uses", "help")

def setup(client):
    client.add_cog(help(client))