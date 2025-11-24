import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class KickLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def kick_log(self, member: nextcord.Member) -> None:
        """A log that activates, when someone gets kicked and a kick log is set"""

        if not (kick_log := member.guild.get_channel(int(await db.Server.KICK_LOG.get(member.guild.id) or 0))):
            return

        entry: nextcord.AuditLogEntry | None = None
        entry_count = 0

        async for entry in member.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - KickLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.kick
        ):
            if member.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) ==  100: # 100 is the default limit
                return

        if not entry:
            return

        Logger().action_log(
            member,
            "kick log",
            {"kicked by": str(entry.user.id), "reason": entry.reason or ""}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Kick Log",
            author_icon = entry.user.display_avatar.url,
            fields = [
                EmbedField(
                    "Member kicked:",
                    f"{entry.user.mention} kicked: {entry.target.mention}", # type: ignore
                    False
                ),
                EmbedField(
                    "Reason:",
                    entry.reason or "",
                    False
                )
            ]
        )

        await kick_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("kick log")



def setup(client: SomiBot) -> None:
    client.add_cog(KickLog(client))