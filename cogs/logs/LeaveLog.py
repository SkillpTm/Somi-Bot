###package#import###############################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import time

###self#imports###############################################################################

from lib.db_modules import AuditLogChannelDB, KeywordDB, ReminderDB, CommandUsesDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class LeaveLog(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ###leave#log###########################################################

    @nextcord_C.Cog.listener()
    async def on_member_remove(self,
                               member: nextcord.Member):
        """
        This function deletes someone's keywords, if they leave a server
        Also if the user just left the last server with Somi their reminders
        And if a server has an audit-log-channel set it generates a log message
        """

        self.client.Loggers.action_log(f"Guild: {member.guild.id} ~ User: {member.id} ~ leave_log()")

        KeywordDB().delete_all(member.guild.id, member.id)

        if member.mutual_guilds == []:
            ReminderDB().delete_all(member.id)

        audit_log_id = AuditLogChannelDB().get(member.guild)

        if not audit_log_id:
            return

        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
            if entry.target.id == member.id:
                return

        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
            if entry.target.id == member.id:
                return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            thumbnail = member.display_avatar,
            title = f"Member Left: `{member.display_name}`",
            footer = "DEFAULT_KST_FOOTER",
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

        audit_log_channel = member.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB().uses_update("log_activations", "leave_log")



def setup(client: SomiBot):
    client.add_cog(LeaveLog(client))