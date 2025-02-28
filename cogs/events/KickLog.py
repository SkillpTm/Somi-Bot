import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class KickLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def kick_log(self, member: nextcord.Member) -> None:
        """A log that activates, when someone gets kicked and an audit log is set"""
        
        audit_log_id: int = await ConfigDB(member.guild.id, "AuditLogChannel").get_list(member.guild)

        if not audit_log_id:
            return

        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
            if member.id != entry.target.id:
                return
            
        self.client.Loggers.action_log(Get().log_message(
            member,
            "kick log",
            {"kicked by": str(entry.user.id), "reason": entry.reason}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Kick Log:",
                    f"{entry.user.mention} kicked: {entry.target.mention}",
                    False
                ],

                [
                    "Reason:",
                    entry.reason,
                    False
                ]
            ]
        )

        await member.guild.get_channel(audit_log_id).send(embed=embed)

        CommandUsesDB("log_activations").update("kick log")



def setup(client: SomiBot) -> None:
    client.add_cog(KickLog(client))