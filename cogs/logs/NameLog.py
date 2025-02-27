import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class NameLog(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_member_update(self,
                               member_before: nextcord.Member,
                               member_after: nextcord.Member):
        """This function checks if a user changed their display name, if they did and the server has an audit-log-channel a log message will be generated."""

        if member_before.display_name == member_after.display_name:
            return

        audit_log_id: int = await ConfigDB(member_before.guild.id, "AuditLogChannel").get_list(member_before.guild)

        if not audit_log_id:
            return

        self.client.Loggers.action_log(f"Guild: {member_before.guild.id} ~ User: {member_before.id} ~ name_log()\nBefore: {member_before.display_name} --> After: {member_after.display_name}")

        if member_before.display_name == member_before.name:
            member_name_before = f"`{member_before.name}`"
        else:
            member_name_before = member_before.display_name
 
        if member_after.display_name == member_before.name:
            member_name_after = f"`{member_before.name}`"
        else:
            member_name_after = member_after.display_name

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            thumbnail = member_before.display_avatar,
            title = f"`{member_before.name}` Changed Their Name",
            footer = "DEFAULT_KST_FOOTER",
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

        audit_log_channel = member_before.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB("log_activations").update("name log")



def setup(client: SomiBot):
    client.add_cog(NameLog(client))