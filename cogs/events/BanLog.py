import datetime
import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class BanLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def ban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets banned and an audit log is set"""

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        # check the last audit log entry for bans, to see make sure this was a ban
        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
            if user.id != entry.target.id or (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
                return

        self.client.Loggers.action_log(Get.log_message(
            user,
            "ban log",
            {"guild": str(guild.id), "banned by": str(entry.user.id), "reason": entry.reason}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Ban Log:",
                    f"{entry.user.mention} banned: {entry.target.mention}",
                    False
                ],

                [
                    "Reason:",
                    entry.reason,
                    False
                ]
            ]
        )

        await guild.get_channel(audit_log_id).send(embed=embed)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("ban log")

    ####################################################################################################

    async def unban_log(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """A log that activates, when someone gets unbanned and an audit log is set"""

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.unban):
            if user.id != entry.target.id or (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
                return

        self.client.Loggers.action_log(Get.log_message(
            user,
            "unban log",
            {"guild": str(guild.id), "unbanned by": str(entry.user.id)}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Unban Log:",
                    f"{entry.user.mention} unbanned: `{entry.target.name}` | `({entry.target.id})`",
                    False
                ]
            ]
        )

        await guild.get_channel(audit_log_id).send(embed=embed)

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("unban log")



def setup(client: SomiBot) -> None:
    client.add_cog(BanLog(client))