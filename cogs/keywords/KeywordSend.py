###package#import###############################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import re

###self#imports###############################################################################

from lib.db_modules import CommandUsesDB, HiddenChannelsDB, KeywordDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot


class KeywordSend(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ###keyword#noti###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_message(self,
                         message: nextcord.Message):
        """
        This function sends keyword notis to users:
        1. in the same guild as the message
        2. with the keyword in their list
        3. if the message wasn't in a forbidden channel
        """

        if not Checks().message_in_guild(self.client, message):
            return

        if HiddenChannelsDB().check_channel_inserted(message.guild.id, message.channel.id):
            return

        all_users_keywords: dict = KeywordDB().get_all(message.guild.id, message.author.id)

        for user_id, user_keywords in all_users_keywords.items():
            
            if not message.guild.get_member(user_id):
                continue

            if user_keywords == []:
                continue

            user_keywords_in_content = []

            for keyword in user_keywords:
                if keyword in re.sub('<[^ ]+?>', "", message.content.lower()): # regex -> message without emotes
                    user_keywords_in_content.append(keyword)

            if user_keywords_in_content == []:
                continue

            output_keywords = ""
            last_keyword = user_keywords_in_content.pop()

            if not user_keywords_in_content == []:
                nearly_all_keywords_list = ", ".join(map(str, user_keywords_in_content))
                output_keywords = f"{nearly_all_keywords_list} and {last_keyword}"
                keywords_info = f"Your keywords: `{output_keywords}` have been mentioned in {message.channel.mention} by {message.author.mention}:"

            else:
                output_keywords = last_keyword
                keywords_info = f"Your keyword: `{output_keywords}` has been mentioned in {message.channel.mention} by {message.author.mention}:"

            self.client.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel: {message.channel.id} ~ User: {message.author.id} ~ keyword() {user_id}\n{output_keywords}")

            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = f"Keyword Notification: `{output_keywords}`",
                title_url = message.jump_url,
                description = f"{keywords_info}\n\n__**Message:**__\n{message.content}"[:4096],
                footer = "DEFAULT_KST_FOOTER")

            embed, file_urls = EmbedFunctions().get_attachments(message.attachments, embed, limit = 1)

            noti_user = await self.client.fetch_user(user_id)

            try:
                await noti_user.send(embed=embed)
            except:
                self.client.Loggers.action_warning(f"keyword() {noti_user.id} couldn't be notified, because their pms aren't open to the client")

            CommandUsesDB().uses_update("command_uses", "keyword send")



def setup(client: SomiBot):
    client.add_cog(KeywordSend(client))