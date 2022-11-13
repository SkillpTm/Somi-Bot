###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import HELP_OPTIONS, HELP_OUTPUT, BOT_COLOR
from utilities.partial_commands import embed_builder, deactivate_view_children

class HelpDropdownView(nextcord.ui.View):
    def __init__(self, response):
        self.response: nextcord.Message = response
        super().__init__(timeout = 300)
    
    @nextcord.ui.string_select(placeholder = "select a command", min_values=1, max_values=1, options = HELP_OPTIONS)

    async def callback(self,
                       select,
                       interaction):
        selection = select.values[0]

        print(f"{interaction.user}: /help {selection}")

        embed = embed_builder(title = f"Help for /{selection}",
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Syntax:",
                              field_one_value = HELP_OUTPUT[selection][0],
                              field_one_inline = False,

                              field_two_name = "Info:",
                              field_two_value = HELP_OUTPUT[selection][1],
                              field_two_inline = False)

        await interaction.edit(content=None, embed=embed)

        uses_update("help_selections", f"{selection}")

    async def on_timeout(self):
        await deactivate_view_children(self)



class Help(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###help###########################################################

    @nextcord.slash_command(name='help', description='explanations for all command')
    async def help(self,
                   interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /help")

        response = await interaction.response.send_message("What command do you need help with?", ephemeral=True)
        HelpDropView = HelpDropdownView(response)
        await response.edit("What command do you need help with?", view=HelpDropView)

        uses_update("command_uses", "help")



def setup(client):
    client.add_cog(Help(client))