###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import re

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import get_keywords
from utilities.maincommands import checks, checks_forbidden_channels
from utilities.partial_commands import embed_attachments, embed_builder
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

                    print(f"{interaction.author}: keyword() {noti_user}\n{output_keywords}")

                    if multiple_keywords:
                        keywords_info = f"Your keywords: `{output_keywords}` have been mentioned in {interaction.channel.mention} by {interaction.author.mention}:"
                    elif not multiple_keywords:
                        keywords_info = f"Your keyword: `{output_keywords}` has been mentioned in {interaction.channel.mention} by {interaction.author.mention}:"

                    embed = embed_builder(title = f"Keyword Notification: `{output_keywords}`",
                                          title_url = interaction.jump_url,
                                          despcription = f"{keywords_info}\n\n__**Message:**__\n{interaction.content}"[:4096],
                                          color = BOT_COLOR)

                    await embed_attachments(noti_user, interaction, embed, link_embed = False)

                    uses_update("command_uses", "keyword send")

def setup(client):
    client.add_cog(keyword(client))