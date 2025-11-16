import datetime
import os
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions, Misc
from lib.managers import Logger
from lib.modules import SomiBot



class PurgeLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def purge_log(self, messages: list[nextcord.Message]) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        if not (audit_log := messages[0].guild.get_channel(await db.Server.AUDIT_LOG.get(messages[0].guild.id) or 0)):
            return

        if await db.HiddenChannel._.get_entry(messages[0].channel.id):
            return

        entry: nextcord.AuditLogEntry = None
        entry_count = 0

        async for entry in messages[0].guild.audit_logs(
            limit=PurgeLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - PurgeLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.message_bulk_delete
        ):
            if entry.user:
                break

            if (entry_count := entry_count + 1) == PurgeLog.MAX_AUDIT_ENTIRES_LIMIT:
                return

        if not entry:
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
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Purge Log:",
                    f"{entry.user.mention} purged: `{len(messages)} message(s)` in {entry.target.mention}",
                    False
                ]
            ]
        )

        await (await audit_log.send(embed=embed)).reply(file=nextcord.File(csv_name), mention_author=False)
        await db.Telemetry.AMOUNT.increment("purge log")
        os.remove(csv_name)



def setup(client: SomiBot) -> None:
    client.add_cog(PurgeLog(client))