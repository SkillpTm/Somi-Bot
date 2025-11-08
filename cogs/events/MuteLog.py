import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.managers import Logger
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class MuteLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def mute_log(
        self,
        member_before: nextcord.Member,
        member_after: nextcord.Member
    ) -> None:
        """A log that activates, when someone gets muted and an audit log is set"""

        if member_before.communication_disabled_until == member_after.communication_disabled_until:
            return

        if not (audit_log := member_before.guild.get_channel(await (await DBHandler(self.client.database, server_id=member_before.guild.id).server()).audit_log_get() or 0)):
            return

        entry: nextcord.AuditLogEntry = None
        entry_count = 0

        async for entry in member_before.guild.audit_logs(
            limit=MuteLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - MuteLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.member_update
        ):
            if member_before.id == entry.target.id:
                break

            if (entry_count := entry_count + 1) == MuteLog.MAX_AUDIT_ENTIRES_LIMIT:
                return

        if member_after.communication_disabled_until:
            embed = self.muted(entry, member_after)
        else:
            embed = self.unmuted(entry, member_after)

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("mute log")

    ####################################################################################################

    def muted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member
    ) -> None:
        """creates the embed, for if the user was muted"""

        Logger().action_log(
            member_after,
            "mute log",
            {
                "muted by": str(entry.user.id),
                "until": str(int(time.mktime(member_after.communication_disabled_until.timetuple()))),
                "reason": entry.reason
            }
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Mute Log:",
                    f"{entry.user.mention} muted: {member_after.mention} until: <t:{int(time.mktime(member_after.communication_disabled_until.timetuple()))}:F>",
                    False
                ],

                [
                    "Reason:",
                    entry.reason,
                    False
                ]
            ]
        )

        return embed

    ####################################################################################################

    def unmuted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member,
    ) -> None:
        """creates the embed, for if the user was unmuted"""

        Logger().action_log(
            member_after,
            "unmute log",
            {"unmuted by": str(entry.user.id)}
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            fields = [
                [
                    "Unmute Log:",
                    f"{entry.user.mention} unmuted: {member_after.mention}",
                    False
                ]
            ]
        )

        return embed




def setup(client: SomiBot) -> None:
    client.add_cog(MuteLog(client))