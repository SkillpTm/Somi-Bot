###package#import###############################################################################

import nextcord
import re

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import get_keywords
from utilities.maincommands import checks, checks_forbidden_channels
from utilities.partial_commands import embed_attachments, embed_builder
from utilities.variables import BOT_COLOR



class KeywordSend(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###keyword#noti###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_message(self,
                         message):
        if not checks(message.guild, message.author):
            return

        if not checks_forbidden_channels(message.channel):
            return

        all_users_keywords = get_keywords(message.author.id)

        #TODO only add keywords of users in this server
        for user_id in all_users_keywords.keys():
            #check if user is in server
            if message.guild.get_member(user_id) != None:
                #check if user has keywords
                if not all_users_keywords[user_id] == []:
                    all_user_keywords = all_users_keywords[user_id]
                    all_user_keywords_in_content = []

                    for keyword in all_user_keywords:
                        if keyword in re.sub(":.*?:", "", str(message.content.lower())): # regex -> message without emotes
                            all_user_keywords_in_content.append(keyword)

                    if all_user_keywords_in_content != []:
                        output_keywords = ""
                        last_keyword = all_user_keywords_in_content.pop()

                        #check if it's only 1 keyword
                        if not all_user_keywords_in_content == []:
                            nearly_all_keywords_list = ", ".join(map(str,all_user_keywords_in_content))
                            output_keywords = f"{nearly_all_keywords_list} and {last_keyword}"
                            multiple_keywords = True
                        else:
                            output_keywords = last_keyword
                            multiple_keywords = False

                        noti_user = await self.client.fetch_user(user_id)

                        print(f"{message.author}: keyword() {noti_user}\n{output_keywords}")

                        if multiple_keywords:
                            keywords_info = f"Your keywords: `{output_keywords}` have been mentioned in {message.channel.mention} by {message.author.mention}:"
                        else:
                            keywords_info = f"Your keyword: `{output_keywords}` has been mentioned in {message.channel.mention} by {message.author.mention}:"

                        embed = embed_builder(title = f"Keyword Notification: `{output_keywords}`",
                                              title_url = message.jump_url,
                                              description = f"{keywords_info}\n\n__**Message:**__\n{message.content}"[:4096],
                                              color = BOT_COLOR,
                                              footer = "DEFAULT_KST_FOOTER")

                        await embed_attachments(noti_user, message, embed)

                        uses_update("command_uses", "keyword send")



def setup(client):
    client.add_cog(KeywordSend(client))