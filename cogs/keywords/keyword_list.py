###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import list_keyword
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, get_user_avatar, embed_builder
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

        while i < amount:
            output += f"{i + 1}. `{keywords_list[i]}`\n"
            i += 1

        member = interaction.guild.get_member(interaction.user.id)
        name = get_nick_else_name(member)
        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = BOT_COLOR,
                              author = f"Keyword List for: `{name}`",
                              author_icon = member_avatar_url,

                              field_one_name = "Keywords:",
                              field_one_value = output[:1000],
                              field_one_inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "keyowrd list")

def setup(client):
    client.add_cog(keyword_list(client))