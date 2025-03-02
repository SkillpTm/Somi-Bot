import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class EditLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def edit_log(
        self,
        message_before: nextcord.Message,
        message_after: nextcord.Message
    ) -> None:
        """This function will create an edit-log message, if a guild has an audit-log-channel and if the message wasn't in a hidden-channel."""

        if not Checks.message_in_guild(self.client, message_before):
            return
        
        if message_before.author.id == self.client.user.id:
            return

        audit_log_id: int = await ConfigDB(message_before.guild.id, "AuditLogChannel").get_list(message_before.guild)

        if not audit_log_id:
            return

        if message_before.channel.id in await ConfigDB(message_before.guild.id, "HiddenChannels").get_list(message_before.guild):
            return

        # content may be the same, if an embed changed
        if message_before.content == message_after.content:
            return

        self.client.Loggers.action_log(Get.log_message(
            message_before,
            "edit log",
            {"message_before": message_before.content, "message_after": message_after.content}
        ))

        first_embed: nextcord.Embed = None
        second_embed: nextcord.Embed = None
        file_urls: str = ""

        if len(message_before.content) < 1024 and len(message_after.content) < 1024:
            first_embed, file_urls = self.single_response(message_before, message_after)
        else:
            first_embed, second_embed, file_urls = self.multi_response(message_before, message_after)

        last_sent_response = await message_before.guild.get_channel(audit_log_id).send(embed=first_embed)

        # there is only a second embed for larger message edits
        if second_embed:
            last_sent_response = await last_sent_response.reply(embed=second_embed)

        if file_urls:
            await last_sent_response.reply(content=file_urls, mention_author=False)

        CommandUsesDB("log_activations").update("edit log")

    ####################################################################################################

    @staticmethod
    async def single_response(
        message_before: nextcord.Message,
        message_after: nextcord.Message
    ) -> tuple[nextcord.Embed, str]:
        """takes in smaller message edits and displays them in a singular embed with fields"""

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Message Edited",
            author_icon = message_before.author.display_avatar.url,
            description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Before:",
                    message_before.content,
                    False
                ],

                [
                    "After:",
                    message_after.content,
                    False
                ]
            ]
        )

        embed, file_urls = EmbedFunctions.get_attachments(message_before.attachments, embed)
        return embed, file_urls
    
    ####################################################################################################

    @staticmethod
    async def multi_response(
        message_before: nextcord.Message,
        message_after: nextcord.Message
    ) -> tuple[nextcord.Embed, nextcord.Embed, str]:
        """takes in bigger message edits and displays them in two embed with the description (one embed for before and another for after)"""

        embed_before = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Message Edited",
            author_icon = message_before.author.display_avatar.url,
            description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})\n**Before:**\n{message_before.content}"[:4095]
        )

        embed_after = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            description = f"**After:**\n{message_after.content}",
            footer = "DEFAULT_KST_FOOTER"
        )

        embed_after, file_urls = EmbedFunctions.get_attachments(message_before.attachments, embed_after)

        return embed_before, embed_after, file_urls



def setup(client: SomiBot) -> None:
    client.add_cog(EditLog(client))