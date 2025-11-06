import datetime
import os
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get, Misc
from lib.utilities import SomiBot



class PurgeLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def purge_log(self, messages: list[nextcord.Message]) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        if not (audit_log := messages[0].guild.get_channel(await (await DBHandler(self.client.database, server_id=messages[0].guild.id).server()).audit_log_get() or 0)):
            return

        if messages[0].channel.id in await (await DBHandler(self.client.database, server_id=messages[0].guild.id).hidden_channel()).get_list():
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

        self.client.logger.action_log(Get.log_message(
            messages[0],
            "purge log",
            {"amount": str(len(messages))}
        ))

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
        os.remove(csv_name)

        await (await DBHandler(self.client.database).telemetry()).increment("purge log")



def setup(client: SomiBot) -> None:
    client.add_cog(PurgeLog(client))