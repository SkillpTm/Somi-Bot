import datetime
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class LeaveLog(nextcord_C.Cog):

    MAX_AUDIT_ENTIRES_LIMIT = 10
    MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def leave_log(self, member: nextcord.Member) -> None:
        """
        This function deletes someone's keywords, if they leave a server
        Also if the user just left the last server with Somi their reminders
        And if a server has an audit-log-channel set it posts a log message
        """

        Logger().action_log(
            member,
            "leave log",
            {"member": str(member.id)}
        )

        if not (audit_log := member.guild.get_channel(await (await DBHandler(self.client.database, server_id=member.guild.id).server()).audit_log_get() or 0)):
            return

        # check the last audit log entry for bans, to see if this was a ban (bans get handled by BanLog)
        async for entry in member.guild.audit_logs(
            limit=LeaveLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - LeaveLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.ban
        ):
            if entry.target.id == member.id:
                return

        # check the last audit log entry for kicks, to see if this was a kick (kicks get handled by KickLog)
        async for entry in member.guild.audit_logs(
            limit=LeaveLog.MAX_AUDIT_ENTIRES_LIMIT,
            after=datetime.datetime.fromtimestamp(time.time() - LeaveLog.MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.kick
        ):
            if entry.target.id == member.id:
                return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            thumbnail = member.display_avatar.url,
            title = f"Member Left: `{member.display_name}`",
            fields = [
                [
                    "ID:",
                    member.id,
                    False
                ],

                [
                    "Name:",
                    member.mention,
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Joined at",
                    f"<t:{int(time.mktime(member.joined_at.timetuple()))}>",
                    True
                ]
            ]
        )

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("leave log")



def setup(client: SomiBot) -> None:
    client.add_cog(LeaveLog(client))