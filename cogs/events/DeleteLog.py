import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class DeleteLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def message_delete_log(self, message: nextcord.Message) -> None:
        """This function will create a delete-log message, if a guild has an audit-log-channel and if the message wasn't in a hidden-channel."""

        if not message.guild:
            return

        if not message.content and len(message.attachments) < 1:
            return

        if not (audit_log := message.guild.get_channel(int(await db.Server.AUDIT_LOG.get(message.guild.id) or 0))):
            return

        if await db.HiddenChannel._.get_entry(message.channel.id):
            return

        # check the last audit log entry for message removals, to see make sure this was a deletion or removal
        async for entry in message.guild.audit_logs(
            limit=DeleteLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - DeleteLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.message_delete
        ):
            if message.author.id == entry.target.id and message.author.id != entry.user.id:
                await self.remove_log(message, audit_log, entry) # type: ignore
                return

        await self.delete_log(message, audit_log) # type: ignore


    async def delete_log(
        self,
        message: nextcord.Message,
        audit_log: nextcord.TextChannel
    ) -> None:
        """logs a deleted message"""

        Logger().action_log(
            message,
            "delete log",
            {"message": message.content}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Message Deleted",
            author_icon = message.author.display_avatar.url,
            description = f"{message.author.mention} deleted a message in: {message.channel.mention}\n\n{message.content}", # type: ignore
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await audit_log.send(embed=embed)

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await db.Telemetry.AMOUNT.increment("delete log")


    async def remove_log(
        self,
        message: nextcord.Message,
        audit_log: nextcord.TextChannel,
        entry: nextcord.AuditLogEntry
    ) -> None:
        """logs a removed message"""

        Logger().action_log(
            message,
            "remove log",
            {"message": message.content, "removed by": str(entry.user.id)}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Message Removed",
            author_icon = entry.user.display_avatar.url,
            description = f"{entry.user.mention} removed a message from {message.author.mention} in: {message.channel.mention}\n\n{message.content}" # type: ignore
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await audit_log.send(embed=embed)

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await db.Telemetry.AMOUNT.increment("remove log")



def setup(client: SomiBot) -> None:
    client.add_cog(DeleteLog(client))