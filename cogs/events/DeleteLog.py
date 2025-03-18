import datetime
import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class DeleteLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def message_delete_log(self, message: nextcord.Message) -> None:
        """This function will create a delete-log message, if a guild has an audit-log-channel and if the message wasn't in a hidden-channel."""

        if not message.guild:
            return

        if not message.content and len(message.attachments) < 1:
            return

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        if message.channel.id in await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).hidden_channel()).get_list():
            return
        
        # check the last audit log entry for message removals, to see make sure this was a deletion or removal
        async for entry in message.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.message_delete):
            if message.author.id == entry.target.id and (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
                await self.remove_log(message, audit_log_id, entry)
            else:
                await self.delete_log(message, audit_log_id)

    ####################################################################################################

    async def delete_log(
        self,
        message: nextcord.Message,
        audit_log_id: int
    ) -> None:
        """logs a deleted message"""

        self.client.Loggers.action_log(Get.log_message(
            message,
            "delete log",
            {"message": message.content}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Message Deleted",
            author_icon = message.author.display_avatar.url,
            description = f"{message.author.mention} deleted a message in: {message.channel.mention}\n\n{message.content}",
            footer = "DEFAULT_KST_FOOTER"
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await message.guild.get_channel(audit_log_id).send(embed=embed)

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("delete log")

    ####################################################################################################

    async def remove_log(
        self,
        message: nextcord.Message,
        audit_log_id: int,
        entry: nextcord.AuditLogEntry
    ) -> None:
        """logs a removed message"""

        self.client.Loggers.action_log(Get.log_message(
            message,
            "remove log",
            {"message": message.content, "removed by": str(entry.user.id)}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Message Removed",
            author_icon = entry.user.display_avatar.url,
            description = f"{entry.user.mention} removed a message from {message.author.mention} in: {message.channel.mention}\n\n{message.content}",
            footer = "DEFAULT_KST_FOOTER"
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)
        sent_message = await message.guild.get_channel(audit_log_id).send(embed=embed)

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("remove log")



def setup(client: SomiBot) -> None:
    client.add_cog(DeleteLog(client))