import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class BanLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def ban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets banned and an audit log is set"""

        if not (audit_log := guild.get_channel(await (await DBHandler(self.client.database, server_id=guild.id).server()).audit_log_get() or 0)):
            return

        entry: nextcord.AuditLogEntry = None
        entry_count = 0

        # check the last audit log entry for bans, to see make sure this was a ban
        async for entry in guild.audit_logs(
            limit=BanLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - BanLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.ban
        ):
            if user.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) == BanLog.MAX_AUDIT_ENTIRES_LIMIT:
                return

        if not entry:
            return

        self.client.logger.action_log(Get.log_message(
            user,
            "ban log",
            {"guild": str(guild.id), "banned by": str(entry.user.id), "reason": entry.reason}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Ban Log:",
                    f"{entry.user.mention} banned: {entry.target.mention}",
                    False
                ],

                [
                    "Reason:",
                    entry.reason,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("ban log")

    ####################################################################################################

    async def unban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets unbanned and an audit log is set"""

        if not (audit_log := guild.get_channel(await (await DBHandler(self.client.database, server_id=guild.id).server()).audit_log_get() or 0)):
            return

        entry: nextcord.AuditLogEntry = None
        entry_count = 0

        async for entry in guild.audit_logs(
            limit=BanLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - BanLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.unban
        ):
            if user.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) == BanLog.MAX_AUDIT_ENTIRES_LIMIT:
                return

        if not entry:
            return

        self.client.logger.action_log(Get.log_message(
            user,
            "unban log",
            {"guild": str(guild.id), "unbanned by": str(entry.user.id)}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Unban Log:",
                    f"{entry.user.mention} unbanned: `{entry.target.name}` | `({entry.target.id})`",
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("unban log")



def setup(client: SomiBot) -> None:
    client.add_cog(BanLog(client))