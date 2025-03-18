import nextcord
import nextcord.ext.commands as nextcord_C
import time

from lib.dbModules import DBHandler
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

        self.client.Loggers.action_log(Get.log_message(
            member,
            "join log",
            {"member": str(member.id)}
        ))


        default_role_id = await (await DBHandler(self.client.PostgresDB, server_id=member.guild.id).server()).default_role_get()

        if default_role_id and not member.bot:
            await member.add_roles(member.guild.get_role(default_role_id))

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=member.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            thumbnail = member.display_avatar.url,
            title = f"New Member Joined: `{member.display_name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "ID:",
                    f"`{member.id}`",
                    False
                ],

                [
                    "Username:",
                    member.name,
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Public Flags:",
                    ", ".join(flag.name for flag in member.public_flags.all()),
                    False
                ]
            ]
        )

        await member.guild.get_channel(audit_log_id).send(embed=embed)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("join log")



def setup(client: SomiBot) -> None:
    client.add_cog(JoinLog(client))