import asyncio
import googleapiclient.discovery
import nextcord
import nextcord.ext.commands as nextcord_C
import time
import os
import requests
import spotipy
import sys
import time
import wolframalpha

from lib.dbModules import DBHandler, PostgresDB
from lib.modules import EmbedFunctions
from lib.utilities import Keychain, Lists, Loggers, Config



class SomiBot(nextcord_C.Bot):

    # Meta
    BOT_GITHUB = Config.BOT_GITHUB
    BOT_INVITE = Config.BOT_INVITE
    BOT_PP = Config.BOT_PP
    BOT_TOS = Config.BOT_TOS
    SOMICORD_INVITE = Config.SOMICORD_INVITE
    SUPPORT_SERVER_ID = Config.SUPPORT_SERVER_ID
    SUPPORT_SERVER_ERRORS_ID = Config.SUPPORT_SERVER_ERRORS_ID
    SUPPORT_SERVER_FEEDBACK_ID = Config.SUPPORT_SERVER_FEEDBACK_ID
    SUPPORT_SERVER_LOGS_ID = Config.SUPPORT_SERVER_LOGS_ID
    VERSION = Config.VERSION

    # Colors
    BOT_COLOR = Config.BOT_COLOR
    GENIUS_COLOR = Config.GENIUS_COLOR
    LASTFM_COLOR = Config.LASTFM_COLOR
    PERMISSION_COLOR = Config.PERMISSION_COLOR

    # Assets
    BAN_HAMMER_GIF = Config.BAN_HAMMER_GIF
    CLOCK_ICON = Config.CLOCK_ICON
    GENIUS_ICON = Config.GENIUS_ICON
    HEADPHONES_ICON = Config.HEADPHONES_ICON
    DEFAULT_PFP = Config.DEFAULT_PFP
    LASTFM_ICON = Config.LASTFM_ICON
    LINK_EMBED_ICON = Config.LINK_EMBED_ICON
    OPENWEATHERMAP_ICON = Config.OPENWEATHERMAP_ICON
    SOMI_BEST_GRILL_IMAGE = Config.SOMI_BEST_GRILL_IMAGE
    SPOTIFY_ICON = Config.SPOTIFY_ICON

    # SOMICORD
    SOMICORD_ID = Config.MODMAIL_SERVER_ID
    SOMICORD_MOD_CHANNEL_ID = Config.MODMAIL_CHANNEL_ID
    SOMICORD_WELCOME_CHANNEL_ID = Config.WELCOME_CHANNEL_ID
    SOMICORD_WELCOME_GIF = Config.SOMICORD_WELCOME_GIF

    # Emotes
    HEADS_EMOTE = Config.HEADS_EMOTE
    REACTION_EMOTE = Config.REACTION_EMOTE
    SOMI_BEST_GRILL_EMOTE = Config.SOMI_BEST_GRILL_EMOTE
    SOMI_F_EMOTE = Config.SOMI_F_EMOTE
    SOMI_ONLY_EMOTE = Config.SOMI_ONLY_EMOTE
    SOMI_WELCOME_EMOTE = Config.SOMI_WELCOME_EMOTE
    TAILS_EMOTE = Config.TAILS_EMOTE

    def __init__(self) -> None:
        # Class imports
        self.Keychain = Keychain()
        self.Lists = Lists(Config.APPLICATION_ID)
        self.Loggers = Loggers()

        # Variables
        self.is_setup = False
        self.start_time = int(time.time())

        super().__init__(
            max_messages = Config.MAX_MESSAGES_CACHE, 
            application_id = Config.APPLICATION_ID,
            intents = nextcord.Intents.all(),
            status = nextcord.Status.online,
            activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=Config.ACTIVITY_NAME),
            allowed_mentions = nextcord.AllowedMentions(everyone=False),
            owner_id = Config.OWNER_ID
        )

        self.add_check(self._global_command_checks)

    ####################################################################################################

    def _api_login(self) -> None:
        """This function adds API logins for Spotify, WolframAlpha and YouTube on the client"""

        self.spotifyOAuth = spotipy.SpotifyOAuth(
            client_id = self.Keychain.SPOTIPY_CLIENT_ID,
            client_secret = self.Keychain.SPOTIPY_CLIENT_SECRET,
            redirect_uri = self.Keychain.SPOTIPY_REDIRECT_URI,
            scope = "user-read-currently-playing"
        )

        self.wolfram_client = wolframalpha.Client(self.Keychain.WOLFRAM_APP_ID)

        self.youtube = googleapiclient.discovery.build(
            "youtube",
            "v3",
            developerKey = self.Keychain.YOUTUBE_API_KEY
        )

    ####################################################################################################

    def _api_logout(self) -> None:
        """Logs the client from the Spotify and YouTube API out"""

        if hasattr(self, "spotifyOAuth"):
            self.spotifyOAuth._session.close()

        if hasattr(self, "youtube"):
            self.youtube.close()

    ####################################################################################################

    async def _apply_missing_default_roles(self) -> None:
        """Checks on all guilds if all users have the default role. This should never be the case, unless someone joined a server during downtime."""

        for guild in self.guilds:
            default_role_id = await (await DBHandler(self.PostgresDB, server_id=guild.id).server()).default_role_get()

            if not default_role_id:
                continue

            default_role = guild.get_role(default_role_id)

            if not default_role:
                continue

            difference = len(guild.humans) == len(default_role.members)

            if difference:
                continue

            for member in guild.humans:
                if not difference:
                    break

                if member not in default_role.members:
                    await member.add_roles(default_role)
                    difference -= 1

    ####################################################################################################

    async def _global_command_checks(self, interaction: nextcord.Interaction) -> bool:
        """checks on all commands for: if the bot is properly setup and if the interaction wasn't cased by a bot"""

        if not self.is_setup:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("The bot is still setting up, please try in a few minutes again!"), ephemeral=True)
            return False
        
        if interaction.user.bot:
            return False
        
        return True

    ####################################################################################################

    async def _start_infinite_loops(self) -> None:
        """This function starts an infinite loop for the ReminderSend cog, which continues until the bot loses internet or gets shutdown"""

        await asyncio.gather(
            self.get_cog("ReminderSend").infinite_reminder_loop()
        )

    ####################################################################################################

    async def on_ready(self) -> None:
        """This function overwrites the build in on_ready function, to login for our APIs and to start all infinite loops"""

        # logout in case this was a restart and we didn't properly exit those API connections
        self._api_logout()
        self.Loggers.bot_status(f"{self.user}: ready and logged in")
        self._api_login()

        self.PostgresDB = await PostgresDB.create("./sql/schema.sql", "./sql/queries.sql", Config.POSTGRES_POOL_MAX_SIZE)

        await self._apply_missing_default_roles()

        self.is_setup = True

        await self._start_infinite_loops()

    ####################################################################################################

    async def on_close(self) -> None:
        """This function overwrites the build in on_close function, to logout from our APIs"""

        self.Loggers.bot_status(f"{self.user}: logged out")

        # attempt to logout the api connections
        try:
            if requests.get("https://www.google.com/").status_code == 200:
                self._api_logout()
        except (requests.ConnectionError):
            pass

        await self.PostgresDB.close()

    ####################################################################################################

    async def on_application_command_completion(self, interaction: nextcord.Interaction) -> None:
        """This function overwrites the build in on_application_command_completion function, to update the usage count of a command with the name of the used application command"""

        command_name: str = ""

        if not hasattr(interaction, "application_command"):
            return

        if hasattr(interaction.application_command, "parent_cmd"):
            command_name += f"{interaction.application_command.parent_cmd.name} "

        if hasattr(interaction.application_command, "name"):
            command_name += f"{interaction.application_command.name}"

        if command_name:
            await (await DBHandler(self.PostgresDB).telemetry()).increment(command_name)

    ####################################################################################################

    async def on_application_command_error(
        self,
        interaction: nextcord.Interaction,
        exception: nextcord.ApplicationError
    ) -> tuple[nextcord.Interaction, nextcord.ApplicationError]:
        """This function overwrites the build in on_application_command_error function, to create a global error log and exception handler."""

        from lib.modules.Get import Get

        self.Loggers.application_command_error(
            exception = exception,
            context = interaction.context,
            created_at = interaction.created_at,
            expires_at = interaction.expires_at,
            type = interaction.type._name_,
            file = interaction.application_command.parent_cog,
            meta_data = Get.log_message(interaction, "error"),
            data = interaction.data,
            app_permissions = interaction.app_permissions.value,
            user_permissions = interaction.permissions.value,
        )

        ERROR_MESSAGE = f"An error has occured while executing this command, make sure {self.user.mention} has all the required permissions. (this includes her role being above others)\n```{exception}```\nA bug-report has been send to the developer."

        if interaction.response.is_done():
            await interaction.followup.send(embed=EmbedFunctions().get_critical_error_message(ERROR_MESSAGE), ephemeral=True)
        else:
            await interaction.response.send_message(embed=EmbedFunctions().get_critical_error_message(ERROR_MESSAGE), ephemeral=True)

        await self.get_guild(self.SUPPORT_SERVER_ID).get_channel(self.SUPPORT_SERVER_ERRORS_ID).send(embed=EmbedFunctions().get_critical_error_message(f"```{exception}```"))

        return await super().on_application_command_error(interaction, exception)

    ####################################################################################################

    async def on_bulk_message_delete(self, messages: list[nextcord.Message]) -> None:
        """This function overwrites the build in on_bulk_message_delete function, to launch the purge_log"""

        await asyncio.gather(
            self.get_cog("PurgeLog").purge_log(messages)
        )

    ####################################################################################################

    async def on_guild_channel_delete(self, channel: nextcord.abc.GuildChannel) -> None:
        """This function overwrites the build in on_guild_channel_delete function, to remove channels from the ConfigDB"""

        await asyncio.gather(
            self.get_cog("ConfigValidate").on_delete(channel)
        )

    ####################################################################################################

    async def on_guild_join(self, guild: nextcord.Guild) -> None:
        """This function overwrites the build in on_guild_join function, to validate we don't have previous server data in the db"""

        await DBHandler(self.PostgresDB, server_id=guild.id).clear_data()

    ####################################################################################################

    async def on_guild_role_delete(self, role: nextcord.Role) -> None:
        """This function overwrites the build in on_guild_role_delete function, to remove threads from the ConfigDB"""

        await asyncio.gather(
            self.get_cog("ConfigValidate").on_delete(role)
        )

    ####################################################################################################

    async def on_member_ban(self, guild: nextcord.Guild,user: nextcord.User) -> None:
        """This function overwrites the build in on_member_ban function, to launch the ban_log"""

        await asyncio.gather(
            self.get_cog("BanLog").ban_log(guild, user),
        )

    ####################################################################################################

    async def on_member_join(self, member: nextcord.Member) -> None:
        """This function overwrites the build in on_member_join function, to launch the join_log and welcome"""

        await asyncio.gather(
            self.get_cog("JoinLog").join_log(member),
            self.get_cog("Welcome").welcome(member),
            DBHandler(self.PostgresDB, user_id=member.id).clear_data() # we clear out potentially old user data
        )

    ####################################################################################################

    async def on_member_remove(self, member: nextcord.Member) -> None:
        """This function overwrites the build in on_member_remove function, to launch the leave_log and the kick_log"""

        await asyncio.gather(
            self.get_cog("LeaveLog").leave_log(member),
            self.get_cog("KickLog").kick_log(member)
        )

    ####################################################################################################

    async def on_member_unban(self, guild: nextcord.Guild, user: nextcord.User) -> None:
        """This function overwrites the build in on_member_unban function, to launch the unban_log"""

        await asyncio.gather(
            self.get_cog("BanLog").unban_log(guild, user)
        )

    ####################################################################################################

    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member) -> None:
        """This function overwrites the build in on_member_update function, to launch the name_log and the mute_log"""

        await asyncio.gather(
            self.get_cog("NameLog").name_log(before, after),
            self.get_cog("MuteLog").mute_log(before, after)
        )

    ####################################################################################################

    async def on_message(self, message: nextcord.Message) -> None:
        """This function overwrites the build in on_message function, to launch keyword_send, levels_gain_xp, link_embed, modmail and reaction"""

        await asyncio.gather(
            self.get_cog("KeywordSend").keyword_send(message),
            self.get_cog("LevelsGainXp").levels_gain_xp(message),
            self.get_cog("LinkEmbed").link_embed(message),
            self.get_cog("Modmail").modmail(message),
            self.get_cog("Reactions").reaction(message)
        )

        return await super().on_message(message)
    
    ####################################################################################################

    async def on_message_delete(self, message: nextcord.Message) -> None:
        """This function overwrites the build in on_message_delete function, to launch the message_delete_log"""

        await asyncio.gather(
            self.get_cog("DeleteLog").message_delete_log(message)
        )

    ####################################################################################################

    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message) -> None:
        """This function overwrites the build in on_message_edit function, to launch the edit_log"""

        await asyncio.gather(
            self.get_cog("EditLog").edit_log(before, after)
        )

    ####################################################################################################

    async def on_thread_delete(self, thread: nextcord.Thread) -> None:
        """This function overwrites the build in on_thread_delete function, to remove threads from the ConfigDB"""

        await asyncio.gather(
            self.get_cog("ConfigValidate").on_delete(thread)
        )

    ####################################################################################################

    @staticmethod
    async def on_thread_join(thread: nextcord.Thread):
        """This function overwrites the build in on_thread_join, so that the client automatically joins all new threads."""

        try:
            await thread.join()
        except:
            pass

    ####################################################################################################

    @staticmethod
    def restart() -> None:
        """This function will restart the bot, by closing and reopening the main file"""

        os.execv(sys.executable, ["python"] + sys.argv)