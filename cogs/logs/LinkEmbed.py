####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import pytz
import re

####################################################################################################

from lib.db_modules import HiddenChannelsDB, CommandUsesDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class LinkEmbed(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_message(self,
                         message: nextcord.Message):
        """This function will automatically create an embed for a message form a link, in the same server, if the message doesn't originate form a hidden-channel."""

        if not Checks.message_in_guild(self.client, message):
            return

        if not f"discord.com/channels/{message.guild.id}" in str(message.content):
            return

        link = re.search(fr'https?://(canary\.)?discord\.com/channels/{message.guild.id}\S+', message.content).group()
        original_message = await Get().message_object_from_link(link, self.client)

        if not original_message:
            return

        if HiddenChannelsDB().check_channel_inserted(message.guild.id, original_message.channel.id):
            return

        if original_message.content == "" and len(original_message.attachments) == 0:
            return

        self.client.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel: {message.channel.id} ~ User: {message.id} ~ link_embed()\n{link}")

        if len(original_message.content) > 1024:
            message_content = f"{original_message.content[:1021]}..."
        else:
            message_content = original_message.content

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = "Message Embed",
            author_icon = original_message.author.display_avatar,
            description = f"{original_message.channel.mention} - [Link]({link})",
            footer = original_message.created_at.astimezone(pytz.timezone('Asia/Seoul')).strftime("%Y/%m/%d %H:%M:%S %Z"),
            footer_icon = self.client.LINK_EMBED_ICON,
            fields = [
                [
                    f"{original_message.author.name} said:",
                    message_content[:1024],
                    False
                ]
            ]
        )

        embed, file_urls = EmbedFunctions().get_attachments(original_message.attachments, embed, limit = 1)
        await message.reply(embed=embed, mention_author=False)

        CommandUsesDB().uses_update("log_activations", "auto embed")



def setup(client: SomiBot):
    client.add_cog(LinkEmbed(client))