import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Config, Logger
from lib.modules import SomiBot



class DeleteLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def message_delete_log(self, message: nextcord.Message) -> None:
        """This function will create a delete-log message, if a server has a delete log and if the message wasn't in a hidden-channel."""

        if not message.guild:
            return

        if not message.content and len(message.attachments) < 1:
            return

        if await db.HiddenChannel._.get_entry(message.channel.id):
            return

        # check the last log entry for message removals, to see make sure this was a deletion or removal
        async for entry in message.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - DeleteLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.message_delete
        ):
            if message.author.id == entry.target.id and message.author.id != entry.user.id:
                await self.send_remove_log(message, entry.user) # type: ignore
                return

        await self.send_delete_log(message) # type: ignore


    @staticmethod
    async def send_delete_log(message: nextcord.Message) -> None:
        """logs a deleted message"""

        if not (delete_log := message.guild.get_channel(int(await db.Server.DELETE_LOG.get(message.guild.id) or 0))):
            return

        Logger().action_log(
            message,
            "delete log",
            {"message": message.content}
        )

        embed = EmbedFunctions.builder(
            color = nextcord.Color.brand_red(),
            author = "Delete Log",
            author_icon = message.author.display_avatar.url,
            description = f"{message.author.mention} deleted a message in: {message.channel.mention}\n\n{message.content}", # type: ignore
            footer = "Originally sent:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = message.created_at
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await delete_log.send(embed=embed) # type: ignore

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await db.Telemetry.AMOUNT.increment("delete log")


    @staticmethod
    async def send_remove_log(message: nextcord.Message, remover: nextcord.User) -> None:
        """logs a removed message"""

        if not (remove_log := message.guild.get_channel(int(await db.Server.REMOVE_LOG.get(message.guild.id) or 0))):
            return

        Logger().action_log(
            message,
            "remove log",
            {"message": message.content, "removed by": str(remover.id)}
        )

        embed = EmbedFunctions.builder(
            color = nextcord.Color.brand_red(),
            author = "Remove Log",
            author_icon = remover.display_avatar.url,
            description = f"{remover.mention} removed a message from {message.author.mention} in: {message.channel.mention}\n\n{message.content}", # type: ignore
            footer = "Originally sent:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = message.created_at
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await remove_log.send(embed=embed) # type: ignore

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await db.Telemetry.AMOUNT.increment("remove log")



def setup(client: SomiBot) -> None:
    client.add_cog(DeleteLog(client))