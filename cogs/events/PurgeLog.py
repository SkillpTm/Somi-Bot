import datetime
import os
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, Misc
from lib.managers import Config, Logger
from lib.modules import SomiBot



class PurgeLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def purge_log(self, messages: list[nextcord.Message]) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        if not messages[0].guild.get_channel(int(await db.Server.PURGE_LOG.get(messages[0].guild.id) or 0)):
            return

        if await db.HiddenChannel._.get_entry(messages[0].channel.id):
            return

        entry: nextcord.AuditLogEntry | None = None
        entry_count = 0

        async for entry in messages[0].guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - PurgeLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.message_bulk_delete
        ):
            if entry.user:
                break

            if (entry_count := entry_count + 1) ==  100: # 100 is the default limit
                return

        if not entry or entry.user.id == self.client.user.id:
            return

        await self.send_purge_log(messages, entry.user) # type: ignore


    @staticmethod
    async def send_purge_log(messages: list[nextcord.Message], purger: nextcord.User | nextcord.Member) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        if not (purge_log := messages[0].guild.get_channel(int(await db.Server.PURGE_LOG.get(messages[0].guild.id) or 0))):
            return

        Logger().action_log(
            messages[0],
            "purge log",
            {"amount": str(len(messages))}
        )

        # we create the csv first to reduce delay between the inital embed and the csv response message
        csv_name = Misc.make_bulk_messages_csv(messages)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Purge Log",
            author_icon = purger.display_avatar.url,
            footer = "Purged until:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = messages[len(messages)-1].created_at,
            fields = [
                EmbedField(
                    "Messages Purged:",
                    f"{purger.mention} purged: `{len(messages)} message(s)` in {messages[0].channel.mention}", # type: ignore
                    False
                )
            ]
        )

        await (await purge_log.send(embed=embed)).reply(file=nextcord.File(csv_name), mention_author=False) # type: ignore
        await db.Telemetry.AMOUNT.increment("purge log")
        os.remove(csv_name)



def setup(client: SomiBot) -> None:
    client.add_cog(PurgeLog(client))