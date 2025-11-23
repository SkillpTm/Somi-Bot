import asyncio
import datetime
import os
import re
import sys
import time
import typing

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import Database, db
from lib.helpers import EmbedFunctions
from lib.managers import Config, Keychain, Logger, Singleton



class SomiBot(nextcord_C.Bot):
    """Extended Bot class with overwritten methodes and custom attributes"""

    def __init__(self) -> None:
        self.owner_id: int
        self.user: nextcord.ClientUser

        self.is_setup = False
        self.start_time = int(time.time())

        super().__init__(
            max_messages = Config().MAX_MESSAGES_CACHE,
            application_id = Config().APPLICATION_ID,
            intents = nextcord.Intents.all(),
            chunk_guilds_at_startup = True,
            status = nextcord.Status.online,
            activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=Config().ACTIVITY_NAME),
            allowed_mentions = nextcord.AllowedMentions(everyone=False),
            owner_id = Config().OWNER_ID
        )

        self.application_command_before_invoke(self._before_command)
        self.add_application_command_check(self._global_command_checks)


    async def _sync_discord_and_db(self) -> None:
        """This function syncs the discord servers and users with the database and applies missing default roles"""

        unique_servers: set[int] = set()
        unique_users: set[int] = set()

        for guild in self.guilds:
            unique_servers.add(guild.id)

            if not guild.chunked:
                await guild.chunk()

            default_role = guild.get_role(int(await db.Server.DEFAULT_ROLE.get(guild.id) or 0))
            difference = len(guild.humans) - len(default_role.members) if default_role else 0

            for member in guild.humans:
                unique_users.add(member.id)

                if not difference:
                    continue

                if default_role and default_role not in member.roles:
                    await member.add_roles(default_role)
                    difference -= 1

        all_db_guilds: set[int] = set(typing.cast(list[int], await db.Server.ID.get_all()))
        all_db_users: set[int] = set(typing.cast(list[int], await db.User.ID.get_all()))

        for guild_id in all_db_guilds - unique_servers:
            await db.Server._.delete(guild_id)

        for guild_id in unique_servers - all_db_guilds:
            await db.Server._.add({db.Server.ID: guild_id})

        for user_id in all_db_users - unique_users:
            await db.User._.delete(user_id)

        for user_id in unique_users - all_db_users:
            await db.User._.add({db.User.ID: user_id})


    async def _before_command(self, interaction: nextcord.Interaction["SomiBot"]) -> None:
        """This function is called before any application command is executed, to log the command usage and increase statistics"""

        command_name: str = ""

        if not hasattr(interaction, "application_command"):
            return

        if hasattr(interaction.application_command, "parent_cmd"):
            command_name += f"{interaction.application_command.parent_cmd.name} " # type: ignore

        if hasattr(interaction.application_command, "name"):
            command_name += f"{interaction.application_command.name}"

        if not command_name:
            return

        if not interaction.user.bot and interaction.guild and interaction.guild in self.guilds:
            await db.Statistic.COMMANDS.increase({db.Statistic.SERVER: interaction.guild.id, db.Statistic.USER: interaction.user.id}, 1)

        await db.Telemetry.AMOUNT.increment(command_name)
        Logger().action_log(interaction, command_name, interaction.data.get("options", [])) # type: ignore


    async def _global_command_checks(self, interaction: nextcord.Interaction["SomiBot"]) -> bool:
        """checks on all commands for: if the bot is properly setup and if the interaction wasn't created by a bot"""

        if not self.is_setup:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("The bot is still setting up, please try in a few minutes again!"), ephemeral=True)
            return False

        if interaction.user.bot:
            return False

        if (
            interaction.authorizing_integration_owners
            and not interaction.authorizing_integration_owners.get(nextcord.IntegrationType.user_install, None)
            and not self.get_guild(interaction.authorizing_integration_owners.get(nextcord.IntegrationType.guild_install, 0)) # the bot can only get guilds it is in
        ): # type: ignore
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"This command can only be user in servers with {self.user.name}."), ephemeral=True)
            return False

        return True


    async def _start_infinite_loops(self) -> None:
        """This function starts an infinite loop for the ReminderSend cog, which continues until the bot loses internet or gets shutdown"""

        await asyncio.gather(
            self.get_cog("ReminderSend").infinite_reminder_loop() # type: ignore
        )


    async def on_ready(self) -> None:
        """This function overwrites the build in on_ready function, to login for our APIs and to start all infinite loops"""

        # api logout in case this was a restart and we didn't properly exit those API connections
        Singleton.reset(Keychain)

        if not self.is_setup:
            await self._sync_discord_and_db()

        self.is_setup = True

        Logger().bot_status(f"{self.user}: ready and logged in")
        await self._start_infinite_loops()


    async def on_close(self) -> None:
        """This function overwrites the build in on_close function, to logout from our APIs"""

        Logger().bot_status(f"{self.user}: logged out")

        # attempt to logout the api connections
        try:
            if requests.get("https://www.google.com/", timeout=10).status_code == 200:
                Singleton.reset(Keychain)
        except requests.ConnectionError:
            pass

        await Database().close()


    async def on_application_command_error(
        self,
        interaction: nextcord.Interaction["SomiBot"],
        exception: nextcord.ApplicationError
    ) -> None:
        """This function overwrites the build in on_application_command_error function, to create a global error log and exception handler."""

        if isinstance(exception, nextcord.ApplicationCheckFailure):
            return

        meta_data = Logger.get_log_message(interaction, "error") # type: ignore

        Logger().application_command_error(f"- exception: `{exception}`" + (log_context := f"""
            - authorizing_integration_owners: `{interaction.authorizing_integration_owners}`
            - context: `{interaction.context}`
            - created_at: `{interaction.created_at}`
            - expires_at: `{interaction.expires_at}`
            - type: `{interaction.type._name_}`
            - file: `{interaction.application_command.parent_cog}`
            - meta_data: `{meta_data}`
            - app_permissions: `{interaction.app_permissions.value}`
            - user_permissions: `{interaction.permissions.value}`
        """))

        error_message = f"An error has occured while executing this command, make sure {self.user.mention} has all the required permissions. (this includes her role being above others)\n```{exception}```\nA bug-report has been send to the developer."

        if interaction.response.is_done():
            await interaction.followup.send(embed=EmbedFunctions().get_critical_error_message(error_message), ephemeral=True)
        else:
            await interaction.response.send_message(embed=EmbedFunctions().get_critical_error_message(error_message), ephemeral=True)

        await self.get_guild(Config().SUPPORT_SERVER_ID).get_channel(Config().SUPPORT_SERVER_ERRORS_ID).send(embed=EmbedFunctions().get_critical_error_message(f"{log_context}\n```{exception}```")) # type: ignore

        return await super().on_application_command_error(interaction, exception)


    async def on_bulk_message_delete(self, messages: list[nextcord.Message]) -> None:
        """This function overwrites the build in on_bulk_message_delete function, to launch the purge_log"""

        await asyncio.gather(
            self.get_cog("PurgeLog").purge_log(messages) # type: ignore
        )


    async def on_guild_channel_delete(self, channel: nextcord.abc.GuildChannel) -> None:
        """This function overwrites the build in on_guild_channel_delete function, to remove channels from the ConfigDB"""

        if channel.id == await db.Server.AUDIT_LOG.get(channel.guild.id):
            await db.Server.AUDIT_LOG.set(channel.guild.id, None)

        if await db.HiddenChannel._.get_entry(channel.id):
            await db.HiddenChannel._.delete(channel.id)

        if await db.LevelIgnoreChannel._.get_entry(channel.id):
            await db.LevelIgnoreChannel._.delete(channel.id)


    async def on_guild_join(self, guild: nextcord.Guild) -> None:
        """This function overwrites the build in on_guild_join function, to add the server to the db"""

        await db.Server._.add({db.Server.ID: guild.id})


    async def on_guild_remove(self, guild: nextcord.Guild) -> None:
        """This function overwrites the build in on_guild_remove function, to remove the server from the db"""

        await db.Server._.delete({db.Server.ID: guild.id})


    async def on_guild_role_delete(self, role: nextcord.Role) -> None:
        """This function overwrites the build in on_guild_role_delete function, to remove threads from the ConfigDB"""

        if role.id == await db.Server.DEFAULT_ROLE.get(role.guild.id):
            await db.Server.DEFAULT_ROLE.set(role.guild.id, None)

        if await db.LevelRole._.get_entry(role.id):
            await db.LevelRole._.delete(role.id)


    async def on_member_ban(self, guild: nextcord.Guild,user: nextcord.User) -> None:
        """This function overwrites the build in on_member_ban function, to launch the ban_log"""

        await asyncio.gather(
            self.get_cog("BanLog").ban_log(guild, user) # type: ignore
        )


    async def on_member_join(self, member: nextcord.Member) -> None:
        """This function overwrites the build in on_member_join function, to launch the join_log and welcome"""

        await db.User._.add_unique({db.User.ID: member.id}, {db.User.ID: member.id})

        await asyncio.gather(
            self.get_cog("JoinLog").join_log(member), # type: ignore
            self.get_cog("Welcome").welcome(member) # type: ignore
        )


    async def on_member_remove(self, member: nextcord.Member) -> None:
        """This function overwrites the build in on_member_remove function, to launch the leave_log and the kick_log"""

        await asyncio.gather(
            self.get_cog("LeaveLog").leave_log(member), # type: ignore
            self.get_cog("KickLog").kick_log(member) # type: ignore
        )

        # if we share any server with the user, don't delete them from the db
        for guild in self.guilds:
            if not guild.chunked:
                await guild.chunk()

            if guild.get_member(member.id):
                return

        await db.User._.delete({db.User.ID: member.id})


    async def on_member_unban(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """This function overwrites the build in on_member_unban function, to launch the unban_log"""

        await asyncio.gather(
            self.get_cog("BanLog").unban_log(guild, user) # type: ignore
        )


    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member) -> None:
        """This function overwrites the build in on_member_update function, to launch the name_log and the mute_log"""

        await asyncio.gather(
            self.get_cog("NameLog").name_log(before, after), # type: ignore
            self.get_cog("MuteLog").mute_log(before, after) # type: ignore
        )


    async def on_message(self, message: nextcord.Message) -> None:
        """This function overwrites the build in on_message function, to launch keyword_send, levels_gain_xp, link_embed, modmail, reaction and reaction_counter"""

        await asyncio.gather(
            self.get_cog("KeywordSend").keyword_send(message), # type: ignore
            self.get_cog("LevelsGainXp").levels_gain_xp(message), # type: ignore
            self.get_cog("LinkEmbed").link_embed(message), # type: ignore
            self.get_cog("Modmail").modmail(message), # type: ignore
            self.get_cog("Reactions").reaction(message), # type: ignore
            self.get_cog("StatisticCounter").statistic_counter(message) # type: ignore
        )

        return await super().on_message(message)


    async def on_message_delete(self, message: nextcord.Message) -> None:
        """This function overwrites the build in on_message_delete function, to launch the message_delete_log"""

        await asyncio.gather(
            self.get_cog("DeleteLog").message_delete_log(message) # type: ignore
        )

        if not message.guild or message.author.bot:
            return

        MAY_AUDIT_ENTRY_TIME_VARIANCE = 5

        # check the last audit log entry for message removals, to see make sure this was a deletion or removal
        async for entry in message.guild.audit_logs(
            after=datetime.datetime.fromtimestamp(time.time() - MAY_AUDIT_ENTRY_TIME_VARIANCE),
            action=nextcord.AuditLogAction.message_delete
        ):
            if message.author.id == entry.target.id and message.author.id == entry.target.id:
                await db.Statistic.DELETES.increase({db.Statistic.SERVER: message.guild.id, db.Statistic.USER: message.author.id}, 1)
                return


    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message) -> None:
        """This function overwrites the build in on_message_edit function, to launch the edit_log"""

        await asyncio.gather(
            self.get_cog("EditLog").edit_log(before, after) # type: ignore
        )

        if not before.guild or before.author.bot:
            return

        await db.Statistic.EDITS.increase({db.Statistic.SERVER: before.guild.id, db.Statistic.USER: before.author.id}, 1)

    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent) -> None:
        """This function overwrites the build in on_raw_reaction_add function, to increase the reaction statistic"""

        if not payload.guild_id or not payload.member or payload.member.bot:
            return

        await db.Statistic.REACTIONS.increase({db.Statistic.SERVER: payload.guild_id, db.Statistic.USER: payload.user_id}, 1)


    async def on_thread_delete(self, thread: nextcord.Thread) -> None:
        """This function overwrites the build in on_thread_delete function, to remove threads from the ConfigDB"""

        if thread.id == await db.Server.AUDIT_LOG.get(thread.guild.id):
            await db.Server.AUDIT_LOG.set(thread.guild.id, None)

        if await db.HiddenChannel._.get_entry(thread.id):
            await db.HiddenChannel._.delete(thread.id)

        if await db.LevelIgnoreChannel._.get_entry(thread.id):
            await db.LevelIgnoreChannel._.delete(thread.id)


    async def get_message_from_link(self, link: str) -> nextcord.Message | None:
        """Generates a message object from a discord message link input"""

        _, channel_id, message_id = matches.groups() if (matches := re.search(r"/channels/(\d+)/(\d+)/(\d+)", link)) else (None, None, None)

        if not channel_id or not message_id:
            return None

        try:
            message = await (await self.fetch_channel(int(channel_id))).fetch_message(int(message_id)) # type: ignore
        except (nextcord.NotFound, nextcord.Forbidden):
            message = None

        return message


    def joined_time_footer(self, interaction: nextcord.Interaction["SomiBot"]) -> tuple[str, datetime.datetime | None]:
        """Returns the footer info for an embed, showing since when data has been displayed"""

        if interaction.user.joined_at > interaction.guild.get_member(self.user.id).joined_at: # type: ignore
            footer = "Data since you joined this server:"
            footer_time = typing.cast(nextcord.Member, interaction.user).joined_at
        else:
            footer = f"Data since {self.user.name} joined this server:"
            footer_time = interaction.guild.get_member(self.user.id).joined_at

        return footer, footer_time


    @staticmethod
    async def on_thread_join(thread: nextcord.Thread):
        """This function overwrites the build in on_thread_join, so that the client automatically joins all new threads."""

        try:
            await thread.join()
        except nextcord.Forbidden:
            pass


    @staticmethod
    def restart() -> None:
        """This function will restart the bot, by closing and reopening the main file"""

        os.execv(sys.executable, ["python"] + sys.argv)