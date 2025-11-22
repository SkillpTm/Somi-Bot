import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Config
from lib.modules import SomiBot



class LinkEmbed(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def link_embed(self, message: nextcord.Message) -> None:
        """This function will automatically create an embed for a message form a link, in the same server, if the message doesn't originate form a hidden-channel."""

        if not message.guild or message.author.bot:
            return

        if f"discord.com/channels/{message.guild.id}" not in str(message.content):
            return

        # if the message link is surrounded by <> it won't embed
        if re.search(fr"<https?://(canary\.)?discord\.com/channels/{message.guild.id}\S+>", message.content).group():
            return

        # gets the link from a message (works for both discord.com and canary.discord.com)
        link = re.search(fr"https?://(canary\.)?discord\.com/channels/{message.guild.id}\S+", message.content).group()

        if not (original_message := await self.client.get_message_from_link(link)):
            return

        if await db.HiddenChannel._.get_entry(original_message.channel.id):
            return

        # this happens, if the original message is just an embed
        if original_message.content == "" and len(original_message.attachments) == 0:
            return

        message_content = original_message.content

        if len(original_message.content) > 1024:
            message_content = f"{message_content[:1021]}..."


        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = "Message Embed",
            author_icon = original_message.author.display_avatar.url,
            description = f"{original_message.channel.mention} - [Link]({link})", # type: ignore
            footer_timestamp = original_message.created_at,
            footer_icon = Config().LINK_EMBED_ICON,
            fields = [
                EmbedField(
                    f"{original_message.author.display_name} said:",
                    message_content[:1024],
                    False
                )
            ]
        )

        embed, _ = EmbedFunctions.get_or_add_attachments(original_message.attachments, embed, limit = 1)
        await message.reply(embed=embed, mention_author=False)

        await db.Telemetry.AMOUNT.increment("link embed")



def setup(client: SomiBot) -> None:
    client.add_cog(LinkEmbed(client))