import nextcord
import nextcord.ext.commands as nextcord_C
import time

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class MuteLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def mute_log(
        self,
        member_before: nextcord.Member,
        member_after: nextcord.Member
    ) -> None:
        """A log that activates, when someone gets muted and an audit log is set"""

        if member_before.communication_disabled_until == member_after.communication_disabled_until:
            return
        
        audit_log_id: int = await ConfigDB(member_before.guild.id, "AuditLogChannel").get_list(member_before.guild)

        if not audit_log_id:
            return

        async for entry in member_before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.member_update):
            if member_before.id != entry.target.id:
                return

        if member_after.communication_disabled_until:
            embed = self.muted(entry, member_after)
        else:
            embed = self.unmuted(entry, member_after)

        await member_before.guild.get_channel(audit_log_id).send(embed=embed)

        CommandUsesDB("log_activations").update("mute log")

    ####################################################################################################

    async def muted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member
    ) -> None:
        """creates the embed, for if the user was muted"""

        self.client.Loggers.action_log(Get.log_message(
            member_after,
            "mute log",
            {
                "muted by": str(entry.user.id),
                "until": str(int(time.mktime(member_after.communication_disabled_until.timetuple()))),
                "reason": entry.reason
            }
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Mute Log:",
                    f"{entry.user.mention} muted: {member_after.mention} until: <t:{int(time.mktime(member_after.communication_disabled_until.timetuple()))}:F>",
                    False
                ],

                [
                    "Reason:",
                    entry.reason,
                    False
                ]
            ]
        )

        return embed

    ####################################################################################################

    async def unmuted(
        self,
        entry: nextcord.AuditLogEntry,
        member_after: nextcord.Member,
    ) -> None:
        """creates the embed, for if the user was unmuted"""

        self.client.Loggers.action_log(Get.log_message(
            member_after,
            "unmute log",
            {"unmuted by": str(entry.user.id)}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Unmute Log:",
                    f"{entry.user.mention} unmuted: {member_after.mention}",
                    False
                ]
            ]
        )

        return embed




def setup(client: SomiBot) -> None:
    client.add_cog(MuteLog(client))