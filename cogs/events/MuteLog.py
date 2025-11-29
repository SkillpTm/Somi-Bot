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

        if not entry or entry.user.id == self.client.user.id:
            return

        if member_after.communication_disabled_until:
            await self.send_mute_log(entry.user, member_after, entry.reason) # type: ignore
        else:
            await self.send_unmute_log(entry.user, member_after, entry.reason) # type: ignore


    @staticmethod
    async def send_mute_log(muter: nextcord.User | nextcord.Member, muted: nextcord.Member, reason: str = "") -> None:
        """A log that activates, when someone gets muted and a mute log is set"""

        if not (mute_log := muted.guild.get_channel(int(await db.Server.MUTE_LOG.get(muted.guild.id) or 0))):
            return

        Logger().action_log(
            muter,
            "mute log",
            {
                "muted": str(muted.id),
                "until": str(int(time.mktime(muted.communication_disabled_until.timetuple()))),
                "reason": reason
            }
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mute Log",
            author_icon = muter.display_avatar.url,
            footer = "Muted until:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = muted.communication_disabled_until,
            fields = [
                EmbedField(
                    "Member muted:",
                    f"{muter.mention} muted: {muted.mention}",
                    False
                ),
                EmbedField(
                    "Reason:",
                    reason,
                    False
                )
            ]
        )

        await mute_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("mute log")

    @staticmethod
    async def send_unmute_log(unmuter: nextcord.User | nextcord.Member, unmuted: nextcord.Member, reason: str = "") -> None:
        """A log that activates, when someone gets unmuted and an unmute log is set"""

        if not (unmute_log := unmuted.guild.get_channel(int(await db.Server.UNMUTE_LOG.get(unmuted.guild.id) or 0))):
            return

        Logger().action_log(
            unmuter,
            "unmute log",
            {"unmuted": str(unmuted.id)}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Unmute Log",
            author_icon = unmuter.display_avatar.url,
            fields = [
                EmbedField(
                    "Member unmuted:",
                    f"{unmuter.mention} unmuted: {unmuted.mention}",
                    False
                ),
                EmbedField(
                    "Reason:",
                    reason,
                    False
                )
            ]
        )

        await unmute_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("unmute log")




def setup(client: SomiBot) -> None:
    client.add_cog(MuteLog(client))