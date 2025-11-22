import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Config, Logger
from lib.modules import SomiBot


class KeywordSend(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def keyword_send(self, message: nextcord.Message) -> None:
        """
        This function sends keyword notis to users:
        1. in the same guild as the message
        2. with the keyword in their list
        3. if the message wasn't in a forbidden channel
        """

        # check that message is in quild
        if not message.guild or message.author.bot:
            return

        # remove messages from hidden channels
        if await db.HiddenChannel._.get_entry(message.channel.id):
            return

        users_keywords: dict[int, list[str]] = {}

        async for entry in db.Keyword._.get_multiple(where={db.Keyword.SERVER: message.guild.id}):
            if message.author.id == db.Keyword.USER.retrieve(entry):
                return

            if not users_keywords.get(int(db.Keyword.USER.retrieve(entry) or 0), None):
                users_keywords[int(db.Keyword.USER.retrieve(entry) or 0)] = []

            users_keywords[int(db.Keyword.USER.retrieve(entry) or 0)].append(str(db.Keyword.KEYWORD.retrieve(entry)))

        for user_id, user_keywords in users_keywords.items():
            user_keywords_in_content: list[str] = []
            message_content = re.sub("<(a:|:)[a-z0-9_]*:[0-9]*>", "", message.content.lower()) # regex -> message without emotes

            for keyword in user_keywords:
                # we don't want keywords within other words so we check here against that
                if re.search(rf"\b{keyword}\b", message_content):
                    user_keywords_in_content.append(f"`{keyword}`")

            # if no keywords found skip user
            if not user_keywords_in_content:
                continue

            # create the output text and preserve output_keywords for the title in the embed
            if len(user_keywords_in_content) > 1:
                output_keywords = ", ".join(user_keywords_in_content[:-1]) + f" and {user_keywords_in_content[-1]}"
                keywords_info = f"{output_keywords} have"
            else:
                output_keywords = f"{user_keywords_in_content[0]}"
                keywords_info = f"{output_keywords} has"

            keywords_info += f"{keywords_info} been mentioned in {message.channel.mention} by {message.author.mention}:" # type: ignore

            embed = EmbedFunctions().builder(
                color = Config().BOT_COLOR,
                title = f"Keyword Notification: {output_keywords}",
                title_url = message.jump_url,
                description = f"{keywords_info}\n\n__**Message:**__\n{message.content}"
            )

            embed, _ = EmbedFunctions.get_or_add_attachments(message.attachments, embed, limit = 1)

            try:
                await self.client.fetch_user(user_id).send(embed=embed) # type: ignore
            except nextcord.Forbidden:
                Logger().action_warning(f"keyword send ~ User: {user_id} couldn't be notified, because their pms aren't open to the client")

            await db.Telemetry.AMOUNT.increment("keyword send")



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordSend(client))