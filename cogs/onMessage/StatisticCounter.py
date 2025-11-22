import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.modules import SomiBot



class StatisticCounter(nextcord_C.Cog):

    emoji_pattern = re.compile(r"<(a:|:)[a-z0-9_]*:[0-9]*>", re.IGNORECASE)
    link_pattern = re.compile(r"https?://((?![-])[a-z0-9-]+\.)+[a-z]+(/?)", re.IGNORECASE)
    words_pattern = re.compile(r"\b\w+\b")

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def statistic_counter(self, message: nextcord.Message) -> None:
        """Counts various statistics from messages sent in guilds where the bot is present"""

        if not message.guild or message.guild not in self.client.guilds or message.author.bot:
            return

        await db.Statistic._.increase(
            {
                db.Statistic.SERVER: message.guild.id,
                db.Statistic.USER: message.author.id
            },
            {
                db.Statistic.ATTACHMENTS: len(message.attachments),
                db.Statistic.CHARS: len(re.sub(self.emoji_pattern, "_",message.content)),
                db.Statistic.EMOTES: len(list(re.finditer(self.emoji_pattern, message.content, re.IGNORECASE))),
                db.Statistic.LINKS: len(list(re.finditer(self.link_pattern, message.content, re.IGNORECASE))),
                db.Statistic.MESSAGES: 1,
                db.Statistic.REPLIES: 1 if message.reference and message.reference.type == nextcord.MessageReferenceType.default else 0,
                db.Statistic.STICKERS: len(message.stickers),
                db.Statistic.WORDS: len(re.findall(
                    r"\b\w+\b",
                    re.sub(self.link_pattern, "", re.sub(self.emoji_pattern, "", message.content))
                )),
            }
        )



def setup(client: SomiBot) -> None:
    client.add_cog(StatisticCounter(client))