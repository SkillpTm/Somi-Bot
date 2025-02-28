import nextcord
import nextcord.ext.commands as nextcord_C
import time

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class JoinLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################
    
    async def join_log(self, member: nextcord.Member) -> None:
        """
        This function will:
        - give the new member a default role, if set
        - create a join-log message, if the guild has the audit log setup
        """

        self.client.Loggers.action_log(Get().log_message(
            member,
            "join log",
            {"member": str(member.id)}
        ))


        default_role_id: int = await ConfigDB(member.guild.id, "DefaultRole").get_list(member.guild)

        if default_role_id:
            await member.add_roles(member.guild.get_role(default_role_id))

        audit_log_id: int = await ConfigDB(member.guild.id, "AuditLogChannel").get_list(member.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            thumbnail = member.display_avatar,
            title = f"New Member Joined: `{member.display_name}`",
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
                ]
            ]
        )

        await member.guild.get_channel(audit_log_id).send(embed=embed)

        CommandUsesDB("log_activations").update("join log")



def setup(client: SomiBot) -> None:
    client.add_cog(JoinLog(client))