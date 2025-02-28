import nextcord
import nextcord.ext.commands as nextcord_C
import os
import time

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Create, EmbedFunctions
from lib.utilities import SomiBot



class ExternalLogs(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_member_ban(self,
                            guild: nextcord.Guild,
                            member: nextcord.Member):
        """A log that activates, when someone gets banned without using the bot"""

        audit_log_id: int = await ConfigDB(guild.id, "AuditLogChannel").get_list(guild)

        if not audit_log_id:
            return

        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
            if entry.user.id == self.client.user.id:
                return

            if entry.target.id != member.id:
                return

        self.client.Loggers.action_log(f"Guild: {guild.id} ~ User: {entry.user.id} ~ ban_log() {entry.target.id}\n{entry.reason}")

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
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

        audit_log_channel = guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB("log_activations").update("external log")

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_member_unban(self,
                              guild: nextcord.Guild,
                              member: nextcord.Member):
        """A log that activates, when someone gets unbanned without using the bot"""

        audit_log_id: int = await ConfigDB(guild.id, "AuditLogChannel").get_list(guild)

        if not audit_log_id:
            return

        async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.unban):
            if entry.user.id == self.client.user.id:
                return

            if entry.target.id != member.id:
                return

        self.client.Loggers.action_log(f"Guild: {guild.id} ~ User: {entry.user.id} ~ unban_log() {entry.target.id}")

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Unban Log:",
                    f"{entry.user.mention} unbanned: {entry.target.mention}",
                    False
                ]
            ]
        )

        audit_log_channel = guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB("log_activations").update("external log")

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_member_remove(self,
                               member: nextcord.Member):
        """A log that activates, when someone gets kicked without using the bot"""
        
        audit_log_id: int = await ConfigDB(member.guild.id, "AuditLogChannel").get_list(member.guild)

        if not audit_log_id:
            return

        async for entry in member.guild.audit_logs(limit=1):
            if entry.action != nextcord.AuditLogAction.kick:
                return
                
            if entry.user.id == self.client.user.id:
                return

            if entry.target.id != member.id:
                return

        self.client.Loggers.action_log(f"Guild: {member.guild.id} ~ User: {entry.user.id} ~ kick_log() {entry.target.id}")

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
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

        audit_log_channel = member.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB("log_activations").update("external log")

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_member_update(self,
                               member_before: nextcord.Member,
                               member_after: nextcord.Member):
        """A log that activates, when someone gets muted without using the bot"""

        if member_before.communication_disabled_until == member_after.communication_disabled_until:
            return
        
        audit_log_id: int = await ConfigDB(member_before.guild.id, "AuditLogChannel").get_list(member_before.guild)

        if not audit_log_id:
            return

        async for entry in member_before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.member_update):
            if entry.user.id == self.client.user.id:
                return

            if entry.target.id != member_before.id:
                return

            if entry.before.communication_disabled_until == entry.after.communication_disabled_until:
                return

        if member_after.communication_disabled_until:
            color_mod_action = nextcord.Color.yellow()
            title_mod_action = "Mute Log:"
            mod_action = f"{entry.user.mention} muted: {member_before.mention} until: <t:{int(time.mktime(member_after.communication_disabled_until.timetuple()))}:F>"

            self.client.Loggers.action_log(f"Guild: {member_before.guild.id} ~ User: {entry.user.id} ~ mute_log() {entry.target.id}")
        else:
            color_mod_action = nextcord.Color.green()
            title_mod_action = "Unmute Log:"
            mod_action = f"{entry.user.mention} unmuted: {member_before.mention}"

            self.client.Loggers.action_log(f"Guild: {member_before.guild.id} ~ User: {entry.user.id} ~ unmute_log() {entry.target.id}")

        embed = EmbedFunctions().builder(
            color = color_mod_action,
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    title_mod_action,
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = member_before.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB("log_activations").update("external log")

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_bulk_message_delete(self,
                                     messages: list[nextcord.Message]):
        """A log that activates, when someone gets purged without using the bot"""

        audit_log_id: int = await ConfigDB(messages[0].guild.id, "AuditLogChannel").get_list(messages[0].guild)

        if not audit_log_id:
            return

        if messages[0].channel.id in await ConfigDB(messages[0].guild.id, "HiddenChannels").get_list(messages[0].guild):
            return

        async for entry in messages[0].guild.audit_logs(limit=1, action=nextcord.AuditLogAction.message_bulk_delete):
            if entry.user.id == self.client.user.id:
                return

        self.client.Loggers.action_log(f"Guild: {messages[0].guild.id} ~ Channel: {messages[0].channel.id} ~ User: {entry.user.id} ~ purge_log() {len(messages)}")

        Create().bulk_messages_csv(messages)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Purge Log:",
                    f"{entry.user.mention} purged: `{len(messages)} message(s)` in {entry.target.mention}",
                    False
                ]
            ]
        )

        audit_log_channel = messages[0].guild.get_channel(audit_log_id)
        sent_message = await audit_log_channel.send(embed=embed)
        await sent_message.reply(file=nextcord.File(f"./storage/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{len(messages)}.csv"), mention_author=False)

        os.remove(f"./storage/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{len(messages)}.csv")

        CommandUsesDB("log_activations").update("external log")



def setup(client: SomiBot):
    client.add_cog(ExternalLogs(client))