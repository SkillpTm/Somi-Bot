import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class LeaveLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def leave_log(self, member: nextcord.Member) -> None:
        """A log that activates, when someone leaves a server and a leave log is set"""

        Logger().action_log(
            member,
            "leave log",
            {"member": str(member.id)}
        )

        if not (leave_log := member.guild.get_channel(int(await db.Server.LEAVE_LOG.get(member.guild.id) or 0))):
            return

        # check the last log entry for bans, to see if this was a ban (bans get handled by BanLog)
        async for entry in member.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - LeaveLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.ban
        ):
            if entry.target.id == member.id:
                return

        # check the last log entry for kicks, to see if this was a kick (kicks get handled by KickLog)
        async for entry in member.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - LeaveLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.kick
        ):
            if entry.target.id == member.id:
                return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Leave Log",
            author_icon = member.display_avatar.url,
            fields = [
                EmbedField(
                    "ID:",
                    str(member.id),
                    False
                ),
                EmbedField(
                    "Name:",
                    member.mention,
                    True
                ),
                EmbedField(
                    "Created at:",
                    f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
                    True
                ),
                EmbedField(
                    "Joined at",
                    f"<t:{int(time.mktime(member.joined_at.timetuple()))}>",
                    True
                ),
            ]
        )

        await leave_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("leave log")



def setup(client: SomiBot) -> None:
    client.add_cog(LeaveLog(client))