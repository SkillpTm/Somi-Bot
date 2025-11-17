import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Logger
from lib.modules import SomiBot



class JoinLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    async def join_log(self, member: nextcord.Member) -> None:
        """
        This function will:
        - give the new member a default role, if set
        - create a join-log message, if the guild has the audit log setup
        """

        Logger().action_log(
            member,
            "join log",
            {"member": str(member.id)}
        )

        if not member.bot and (default_role := member.guild.get_role(await db.Server.DEFAULT_ROLE.get(member.guild.id) or 0)):
            await member.add_roles(member.guild.get_role(default_role))

        if not (audit_log := member.guild.get_channel(await db.Server.AUDIT_LOG.get(member.guild.id) or 0)):
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
        await db.Telemetry.AMOUNT.increment("join log")



def setup(client: SomiBot) -> None:
    client.add_cog(JoinLog(client))