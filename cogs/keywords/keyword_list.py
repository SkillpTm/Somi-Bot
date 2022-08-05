###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import list_keyword
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_message_author, embed_get_title_name
from utilities.variables import BOT_COLOR



class keyword_list(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import keyword

    ###keyword#list###########################################################

    @keyword.subcommand(name = "list", description = "A list of all your keywords")
    async def keyword_list(self,
                           interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /keyword list")

        amount, keywords_list = list_keyword(interaction.user.id)

        if amount == 0:
            await interaction.response.send_message("You don't have any keywords.", ephemeral=True)
            return

        output = ""
        i = 0

        title_name = embed_get_title_name(interaction.user)

        embed = Embed(colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_message_author(interaction, embed, f"Keyword List for: {title_name}")

        while i < amount:
            output += f"{i + 1}. `{keywords_list[i]}`\n"
            i += 1
        embed.add_field(name = "Keywords:", value = output[:1000], inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "keyowrd list")

def setup(client):
    client.add_cog(keyword_list(client))