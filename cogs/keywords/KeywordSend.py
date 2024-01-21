###package#import###############################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import re

###self#imports###############################################################################

from lib.db_modules import CommandUsesDB, ConfigDB, KeywordDB
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

        if message.channel.id in await ConfigDB(message.guild.id, "HiddenChannels").get_list(message.guild):
            return

        all_users_keywords = KeywordDB(message.guild.id, message.author.id).get_all()

        for user_id, user_keywords in all_users_keywords.items():
            
            if not user_keywords:
                continue

            if not message.guild.get_member(user_id):
                continue

            user_keywords_in_content: list[str] = []
            message_content = re.sub('<[^ ]+?>', "", message.content.lower()) # regex -> message without emotes

            for keyword in user_keywords:
                if (f" {keyword} " in message_content
                    or message_content.startswith(f"{keyword} ")
                    or message_content.endswith(f" {keyword}")
                    or message_content == f"{keyword}"):
                    user_keywords_in_content.append(f"`{keyword}`")

            if not user_keywords_in_content:
                continue

            if len(user_keywords_in_content) == 1:
                output_keywords = user_keywords_in_content[0]
                keywords_info = f"Your keyword: {output_keywords} has been mentioned in {message.channel.mention} by {message.author.mention}:"
            else:
                last_keyword = user_keywords_in_content.pop()
                output_keywords = f"{', '.join(map(str, user_keywords_in_content))} and {last_keyword}"
                keywords_info = f"Your keywords: {output_keywords} have been mentioned in {message.channel.mention} by {message.author.mention}:"


            self.client.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel: {message.channel.id} ~ User: {message.author.id} ~ keyword() {user_id}\n{output_keywords}")

            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = f"Keyword Notification: {output_keywords}",
                title_url = message.jump_url,
                description = f"{keywords_info}\n\n__**Message:**__\n{message.content}",
                footer = "DEFAULT_KST_FOOTER"
            )

            embed, file_urls = EmbedFunctions().get_attachments(message.attachments, embed, limit = 1)

            noti_user = await self.client.fetch_user(user_id)

            try:
                await noti_user.send(embed=embed)
            except:
                self.client.Loggers.action_warning(f"keyword() {noti_user.id} couldn't be notified, because their pms aren't open to the client")

            CommandUsesDB("command_uses").update("keyword send")



def setup(client: SomiBot):
    client.add_cog(KeywordSend(client))
