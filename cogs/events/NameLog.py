import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
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

        # check if the user's display or username changed
        if member_before.display_name == member_after.display_name and member_before.name == member_after.name:
            return

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=member_before.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        self.client.Loggers.action_log(Get.log_message(
            member_before,
            "leave log",
            {
                "member_before.display_name": member_before.display_name,
                "member_after.display_name": member_after.display_name,
                "member_before.name": member_before.name,
                "member_after.name": member_after.name
            }
        ))

        # indecate if the displayname was just their username or if they changed usernames
        if (member_before.display_name == member_before.name) or (member_before.name != member_after.name):
            member_name_before = f"`{member_before.name}`"
        else:
            member_name_before = member_before.display_name
 
        # indecate if the displayname is now the username  or if they changed usernames
        if (member_after.display_name == member_before.name) or (member_before.name != member_after.name):
            member_name_after = f"`{member_before.name}`"
        else:
            member_name_after = member_after.display_name

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            thumbnail = member_before.display_avatar.url,
            title = f"`{member_before.name}` Changed Their Name",
            fields = [
                [
                    "Name Before:",
                    f"{member_name_before}",
                    False
                ],

                [
                    "Name After:",
                    f"{member_name_after}",
                    False
                ]
            ]
        )

        await member_before.guild.get_channel(audit_log_id).send(embed=embed)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("name log")



def setup(client: SomiBot) -> None:
    client.add_cog(NameLog(client))