###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import list_keyword
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, get_user_avatar, embed_builder
from utilities.variables import BOT_COLOR



class KeywordList(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import keyword

    ###keyword#list###########################################################

    @keyword.subcommand(name = "list", description = "a list of all your keywords")
    async def keyword_list(self,
                           interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /keyword list")

        keywords_list = list_keyword(interaction.user.id)

        if len(keywords_list) == 0:
            await interaction.response.send_message("You don't have any keywords.", ephemeral=True)
            return

        output = ""
        i = 0

        while i < len(keywords_list):
            output += f"{i + 1}. `{keywords_list[i]}`\n"
            i += 1

        member = interaction.guild.get_member(interaction.user.id)
        name = get_nick_else_name(member)
        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = BOT_COLOR,
                              author = f"Keyword List for: `{name}`",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Keywords:",
                              field_one_value = output[:1000],
                              field_one_inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "keyowrd list")



def setup(client):
    client.add_cog(KeywordList(client))