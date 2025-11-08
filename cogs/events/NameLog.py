import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Logger
from lib.utilities import SomiBot



class NameLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def name_log(
        self,
        member_before: nextcord.Member,
        member_after: nextcord.Member
    ) -> None:
        """This function checks if a user changed their display name, if they did and the server has an audit-log-channel a log message will be generated."""

        # check if the user's display-, global- or username changed
        if (member_before.display_name == member_after.display_name) and (member_before.global_name == member_after.global_name) and (member_before.name == member_after.name):
            return

        if not (audit_log := member_before.guild.get_channel(await (await DBHandler(self.client.database, server_id=member_before.guild.id).server()).audit_log_get() or 0)):
            return

        if member_before.name != member_after.name:
            name_type = "Username"
            previous_name = member_before.name
            current_name = member_after.name

        elif member_before.global_name != member_after.global_name:
            name_type = "Display Name"
            previous_name = member_before.global_name or "`None`"
            current_name = member_after.name or "`None`"

        else:
            name_type = "Server Nickname"
            previous_name = member_before.display_name if any(member_before.display_name in [member_before.global_name, member_before.name]) else "`None`"
            current_name = member_after.display_name if any(member_after.display_name in [member_after.global_name, member_after.name]) else "`None`"

        Logger().action_log(
            member_before,
            "name log",
            {
                "name type": name_type,
                "name before": previous_name,
                "name after": current_name,
            }
        )

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            thumbnail = member_before.display_avatar.url,
            title = f"`{member_before.id}` Changed Their {name_type}",
            fields = [
                [
                    f"{name_type} Before:",
                    previous_name,
                    False
                ],

                [
                    f"{name_type} After:",
                    current_name,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

        await (await DBHandler(self.client.database).telemetry()).increment("name log")



def setup(client: SomiBot) -> None:
    client.add_cog(NameLog(client))