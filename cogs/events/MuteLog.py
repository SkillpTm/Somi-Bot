import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Config, Logger
from lib.modules import SomiBot



class MuteLog(nextcord_C.Cog):

    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def mute_log(
        self,
        member_before: nextcord.Member,
        member_after: nextcord.Member
    ) -> None:
        """A log that activates, when someone gets muted/unmuted and a mute log is set"""

        if member_before.communication_disabled_until == member_after.communication_disabled_until:
            return

        if not (mute_log := member_before.guild.get_channel(int(await db.Server.MUTE_LOG.get(member_before.guild.id) or 0))):
            return

        entry: nextcord.AuditLogEntry | None = None
        entry_count = 0

        async for entry in member_before.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - MuteLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.member_update
        ):
            if member_before.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) ==  100: # 100 is the default limit
                return

        if not entry:
            return

        if member_after.communication_disabled_until:
            if not (mute_log := member_before.guild.get_channel(int(await db.Server.MUTE_LOG.get(member_before.guild.id) or 0))):
                return

            await self.muted(entry, member_after, mute_log) # type: ignore
        else:
            if not (unmute_log := member_before.guild.get_channel(int(await db.Server.UNMUTE_LOG.get(member_before.guild.id) or 0))):
                return

            await self.unmuted(entry, member_after, unmute_log) # type: ignore



    async def muted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member,
        mute_log: nextcord.TextChannel | nextcord.Thread
    ) -> None:
        """creates the embed, for if the user was muted"""

        Logger().action_log(
            member_after,
            "mute log",
            {
                "muted by": str(entry.user.id),
                "until": str(int(time.mktime(member_after.communication_disabled_until.timetuple()))),
                "reason": entry.reason or ""
            }
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mute Log",
            author_icon = entry.user.display_avatar.url,
            footer = "Muted until:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = member_after.communication_disabled_until,
            fields = [
                EmbedField(
                    "Member muted:",
                    f"{entry.user.mention} muted: {member_after.mention}",
                    False
                ),
                EmbedField(
                    "Reason:",
                    entry.reason or "",
                    False
                )
            ]
        )

        await mute_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("mute log")


    async def unmuted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member,
        unmute_log: nextcord.TextChannel | nextcord.Thread
    ) -> None:
        """creates the embed, for if the user was unmuted"""

        Logger().action_log(
            member_after,
            "unmute log",
            {"unmuted by": str(entry.user.id)}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Unmute Log",
            author_icon = entry.user.display_avatar.url,
            fields = [
                EmbedField(
                    "Member unmuted:",
                    f"{entry.user.mention} unmuted: {member_after.mention}",
                    False
                )
            ]
        )

        await unmute_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("unmute log")




def setup(client: SomiBot) -> None:
    client.add_cog(MuteLog(client))