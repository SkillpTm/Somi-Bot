import nextcord
import nextcord.ext.commands as nextcord_C
import re
import zoneinfo

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LinkEmbed(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def link_embed(self, message: nextcord.Message) -> None:
        """This function will automatically create an embed for a message form a link, in the same server, if the message doesn't originate form a hidden-channel."""

        if not message.guild:
            return

        if not f"discord.com/channels/{message.guild.id}" in str(message.content):
            return
        
        # if the message link is surrounded by <> it won't embed
        if re.search(fr'<https?://(canary\.)?discord\.com/channels/{message.guild.id}\S+>', message.content).group():
            return

        # gets the link from a message (works for both discord.com and canary.discord.com)
        link = re.search(fr'https?://(canary\.)?discord\.com/channels/{message.guild.id}\S+', message.content).group()
        original_message = await Get.message_object_from_link(link, self.client)

        if not original_message:
            return

        if original_message.channel.id in await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).hidden_channel()).get_list():
            return

        # this happens, if the original message is just an embed
        if original_message.content == "" and len(original_message.attachments) == 0:
            return

        self.client.Loggers.action_log(Get.log_message(
            message,
            "link embed",
            {"link": link}
        ))

        message_content = original_message.content

        if len(original_message.content) > 1024:
            message_content = f"{message_content[:1021]}..."


        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = "Message Embed",
            author_icon = original_message.author.display_avatar.url,
            description = f"{original_message.channel.mention} - [Link]({link})",
            footer = original_message.created_at.astimezone(zoneinfo.ZoneInfo("Asia/Seoul")).strftime("%Y/%m/%d %H:%M:%S %Z"),
            footer_icon = self.client.LINK_EMBED_ICON,
            fields = [
                [
                    f"{original_message.author.display_name} said:",
                    message_content[:1024],
                    False
                ]
            ]
        )

        embed, _ = EmbedFunctions.get_attachments(original_message.attachments, embed, limit = 1)
        await message.reply(embed=embed, mention_author=False)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("link embed")



def setup(client: SomiBot) -> None:
    client.add_cog(LinkEmbed(client))