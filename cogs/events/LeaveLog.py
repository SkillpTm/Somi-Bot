import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import time

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LeaveLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def leave_log(self, member: nextcord.Member) -> None:
        """
        This function deletes someone's keywords, if they leave a server
        Also if the user just left the last server with Somi their reminders
        And if a server has an audit-log-channel set it posts a log message
        """

        self.client.Loggers.action_log(Get.log_message(
            member,
            "leave log",
            {"member": str(member.id)}
        ))

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=member.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        # check the last audit log entry for bans, to see if this was a ban (bans get handled by BanLog)
        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
            if entry.target.id == member.id and (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
                return

        # check the last audit log entry for kicks, to see if this was a kick (kicks get handled by KickLog)
        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
            if entry.target.id == member.id and (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
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

        await member.guild.get_channel(audit_log_id).send(embed=embed)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("leave log")



def setup(client: SomiBot) -> None:
    client.add_cog(LeaveLog(client))