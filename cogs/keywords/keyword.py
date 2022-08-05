###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
import re

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import get_keywords
from utilities.maincommands import checks, checks_forbidden_channels, checks_max_word_length
from utilities.partial_commands import embed_kst_footer, embed_attachments
from utilities.variables import BOT_COLOR



class keyword(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###keyword#noti###########################################################

    @commands.Cog.listener()
    async def on_message(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

        if not checks_forbidden_channels(interaction):
            return

        all_users_keywords = get_keywords(interaction.author.id)

        for key in all_users_keywords.keys():
            if not all_users_keywords[key] == []:
                all_user_keywords = all_users_keywords[key]
                all_user_keywords_in_content = []

                for i in range(len(all_user_keywords)):
                    if all_user_keywords[i] in re.sub(":.*?:", "", str(interaction.content.lower())):
                        all_user_keywords_in_content.append(all_user_keywords[i])

                if len(all_user_keywords_in_content) > 0:
                    output_keywords = ""
                    last_keyword = all_user_keywords_in_content.pop()

                    if not all_user_keywords_in_content == []:
                        nearly_all_keywords_list = ", ".join(map(str,all_user_keywords_in_content))
                        output_keywords = f"{nearly_all_keywords_list} and {last_keyword}"
                        multiple_keywords = True
                    else:
                        output_keywords = last_keyword
                        multiple_keywords = False

                    noti_user = await self.client.fetch_user(key)

                    embed = Embed(title = f"Keyword Notification: `{output_keywords}`",
                                  url = interaction.jump_url,
                                  colour=BOT_COLOR)
                    embed_kst_footer(embed)

                    print(f"{interaction.author}: keyword() {noti_user}\n{output_keywords}")
                    
                    if multiple_keywords:
                        embed.add_field(name = "Reason:", value = f"Your keywords: `{output_keywords}` have been mentioned in {interaction.channel.mention} by {interaction.author.mention}:", inline = False)
                    elif not multiple_keywords:
                        embed.add_field(name = "Reason:", value = f"Your keyword: `{output_keywords}` has been mentioned in {interaction.channel.mention} by {interaction.author.mention}:", inline = False)

                    checks_max_word_length(interaction, embed, source = "keywords")

                    await embed_attachments(noti_user, interaction, embed, link_embed = False)

                    uses_update("command_uses", "keyword send")

def setup(client):
    client.add_cog(keyword(client))