import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class BanLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def ban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets banned and a ban log is set"""

        if not guild.get_channel(int(await db.Server.BAN_LOG.get(guild.id) or 0)):
            return

        entry: nextcord.AuditLogEntry | None = None
        entry_count = 0

        # check the last log entry for bans, to see make sure this was a ban
        async for entry in guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - BanLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.ban
        ):
            if user.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) == 100: # 100 is the default limit
                return

        if not entry or entry.user.id == self.client.user.id:
            return

        await self.send_ban_log(guild, entry.user, user, entry.reason) # type: ignore


    @staticmethod
    async def send_ban_log(guild: nextcord.Guild, banner: nextcord.User | nextcord.Member, banned: nextcord.User, reason: str = "") -> None:
        """A log that activates, when someone gets banned and a ban log is set"""

        if not (ban_log := guild.get_channel(int(await db.Server.BAN_LOG.get(guild.id) or 0))):
            return

        Logger().action_log(
            banner,
            "ban log",
            {"guild": str(guild.id), "banned": str(banned.id), "reason": reason or ""}
        )

        embed = EmbedFunctions.builder(
            color = nextcord.Color.brand_red(),
            author = "Ban Log",
            author_icon = banner.display_avatar.url,
            fields = [
                EmbedField(
                    "Member banned:",
                    f"{banner.mention} banned: {banned.mention}", # type: ignore
                    False
                ),
                EmbedField(
                    "Reason:",
                    reason or "",
                    False
                )
            ]
        )

        await ban_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("ban log")


    async def unban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets unbanned and an unban log is set"""

        if not guild.get_channel(int(await db.Server.UNBAN_LOG.get(guild.id) or 0)):
            return

        entry: nextcord.AuditLogEntry | None = None
        entry_count = 0

        async for entry in guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - BanLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.unban
        ):
            if user.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) ==  100: # 100 is the default limit
                return

        if not entry or entry.user.id == self.client.user.id:
            return

        await self.send_unban_log(guild, entry.user, user, entry.reason) # type: ignore


    @staticmethod
    async def send_unban_log(guild: nextcord.Guild, unbanner: nextcord.User | nextcord.Member, unbanned: nextcord.User, reason: str = "") -> None:
        """A log that activates, when someone gets unbanned and an unban log is set"""

        if not (unban_log := guild.get_channel(int(await db.Server.UNBAN_LOG.get(guild.id) or 0))):
            return

        Logger().action_log(
            unbanner,
            "unban log",
            {"guild": str(guild.id), "unbanned": str(unbanned.id), "reason": reason}
        )

        embed = EmbedFunctions.builder(
            color = nextcord.Color.orange(),
            author = "Unban Log",
            author_icon = unbanner.display_avatar.url,
            fields = [
                EmbedField(
                    "User unbanned:",
                    f"{unbanner.mention} unbanned: `{unbanned.name}` *({unbanned.id})*", # type: ignore
                    False
                ),
                EmbedField(
                    "Reason:",
                    reason,
                    False
                )
            ]
        )

        await unban_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("unban log")



def setup(client: SomiBot) -> None:
    client.add_cog(BanLog(client))