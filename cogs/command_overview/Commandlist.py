###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import COMMAND_LIST, BOT_COLOR
from utilities.partial_commands import embed_builder



class Commandlist(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###commandlist###########################################################

    @nextcord.slash_command(name = "cl", description = "a list of all main commands", name_localizations = {country_tag:"commandlist" for country_tag in nextcord.Locale})
    async def commandlist(self,
                          interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /commandlist")

        embed = embed_builder(title = "A list of all main commands",
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Commands:",
                              field_one_value = COMMAND_LIST,
                              field_one_inline = True,

                              field_two_name = "Help:",
                              field_two_value = "Explanations for singular commands can be found by typing `/help`!",
                              field_two_inline = False)
        
        await interaction.send(embed=embed, ephemeral=True)

        uses_update("command_uses", "commandlist")



def setup(client):
    client.add_cog(Commandlist(client))