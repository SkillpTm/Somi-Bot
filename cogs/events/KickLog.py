import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class KickLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def kick_log(self, member: nextcord.Member) -> None:
        """A log that activates, when someone gets kicked and an audit log is set"""

        if not (audit_log := member.guild.get_channel(await db.Server.AUDIT_LOG.get(member.guild.id) or 0)):
            return

        entry: nextcord.AuditLogEntry = None
        entry_count = 0

        async for entry in member.guild.audit_logs(
            limit=KickLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - KickLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.kick
        ):
            if member.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) == KickLog.MAX_AUDIT_ENTIRES_LIMIT:
                return

        if not entry:
            return


        Logger().action_log(
            member,
            "kick log",
            {"kicked by": str(entry.user.id), "reason": entry.reason}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Kick Log:",
                    f"{entry.user.mention} kicked: {entry.target.mention}",
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
        await db.Telemetry.AMOUNT.increment("kick log")



def setup(client: SomiBot) -> None:
    client.add_cog(KickLog(client))