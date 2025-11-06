import time

import nextcord
import nextcord.ext.commands as nextcord_C

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

        self.client.logger.action_log(Get.log_message(
            member,
            "join log",
            {"member": str(member.id)}
        ))

        if not member.bot and (default_role := member.guild.get_role(await (await DBHandler(self.client.database, server_id=member.guild.id).server()).default_role_get())):
            await member.add_roles(member.guild.get_role(default_role))

        if not (audit_log := member.guild.get_channel(await (await DBHandler(self.client.database, server_id=member.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            thumbnail = member.display_avatar.url,
            title = f"New Member Joined: `{member.display_name}`",
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

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("join log")



def setup(client: SomiBot) -> None:
    client.add_cog(JoinLog(client))