import nextcord
import nextcord.ext.commands as nextcord_C
import re

from lib.db_modules import CommandUsesDB, ConfigDB, KeywordDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot


class KeywordSend(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def keyword_send(self, message: nextcord.Message):
        """
        This function sends keyword notis to users:
        1. in the same guild as the message
        2. with the keyword in their list
        3. if the message wasn't in a forbidden channel
        """

        # check that message is in quild
        if not Checks.message_in_guild(self.client, message) or not Checks.message_not_by_bot(message):
            return

        # remove messages from hidden channels
        if message.channel.id in await ConfigDB(message.guild.id, "HiddenChannels").get_list(message.guild):
            return

        all_users_keywords = KeywordDB(message.guild.id, message.author.id).get_all()

        for user_id, user_keywords in all_users_keywords.items():
            
            # if the user has no keywords or left the guidl skip them
            if not user_keywords or not message.guild.get_member(user_id):
                continue

            user_keywords_in_content: list[str] = []
            message_content = re.sub('<[^ ]+?>', "", message.content.lower()) # regex -> message without emotes

            for keyword in user_keywords:
                # we don't want keywords within other words so we check here against all cases except that.
                if (f" {keyword} " in message_content
                    or message_content.startswith(f"{keyword} ")
                    or message_content.endswith(f" {keyword}")
                    or message_content == f"{keyword}"):
                    user_keywords_in_content.append(f"`{keyword}`")

            # if no keywords found skip user
            if not user_keywords_in_content:
                continue

            self.client.Loggers.action_log(Get.log_message(
                message,
                "/keyword send",
                {"keywords": ", ".join(user_keywords_in_content)}
            ))

            # create the output text and preserve output_keywords for the title in the embed
            if len(user_keywords_in_content) > 1:
                output_keywords = ", ".join(user_keywords_in_content[:-1]) + f" and {user_keywords_in_content[-1]}"
                keywords_info = f"{output_keywords} have"
            else:
                output_keywords = f"{user_keywords_in_content[0]}"
                keywords_info = f"{output_keywords} has"

            keywords_info += f"{keywords_info} been mentioned in {message.channel.mention} by {message.author.mention}:"


            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = f"Keyword Notification: {output_keywords}",
                title_url = message.jump_url,
                description = f"{keywords_info}\n\n__**Message:**__\n{message.content}",
                footer = "DEFAULT_KST_FOOTER"
            )

            embed, _ = EmbedFunctions.get_attachments(message.attachments, embed, limit = 1)

            try:
                await self.client.fetch_user(user_id).send(embed=embed)
            except:
                self.client.Loggers.action_warning(f"keyword send ~ User: {user_id} couldn't be notified, because their pms aren't open to the client")

            CommandUsesDB("command_uses").update("keyword send")



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordSend(client))
