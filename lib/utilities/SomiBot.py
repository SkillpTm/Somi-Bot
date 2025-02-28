import asyncio
import googleapiclient.discovery
import nextcord
import nextcord.ext.commands as nextcord_C
import time
import pylast
import os
import requests
import spotipy
import sys
import time
import wolframalpha

from lib.db_modules.CommandUsesDB import CommandUsesDB
from lib.utilities.Keychain import Keychain
from lib.utilities.Lists import Lists
from lib.utilities.Loggers import Loggers
from storage.Config import Config



class SomiBot(nextcord_C.Bot):

    # Meta
    SOMI_GITHUB = "https://github.com/SkillpTm/Somi-Bot"
    SOMI_TOS = "https://github.com/SkillpTm/Somi-Bot/wiki/Terms-of-Service--of-@Somi%236418"
    SOMI_PP = "https://github.com/SkillpTm/Somi-Bot/wiki/Privacy-Policy-of-@Somi%236418"
    SOMI_CONTACT_EMAIL = "somibot0309@gmail.com"
    SOMI_INVITE = "https://somibot.skillp.dev/invite/"
    SOMICORD_INVITE = "https://discord.gg/Frd7WYg"
    VERSION = "3.1"

    # Colors
    BOT_COLOR = 0xffa6fc
    GENIUS_COLOR = 0xf6f069
    LASTFM_COLOR = 0xd0232b
    MOD_COLOR = nextcord.Color.blue()

    # Assets
    BAN_HAMMER_GIF = "https://somibot.skillp.dev/cdn/gifs/BAN_HAMMER_GIF.gif"
    CLOCK_ICON = "https://somibot.skillp.dev/cdn/images/CLOCK_ICON.png"
    GENIUS_ICON = "https://somibot.skillp.dev/cdn/images/GENIUS_ICON.png"
    DEFAULT_PFP = "https://cdn.discordapp.com/embed/avatars/0.png"
    LASTFM_ICON = "https://somibot.skillp.dev/cdn/images/LASTFM_ICON.png"
    LINK_EMBED_ICON = "https://somibot.skillp.dev/cdn/images/LINK_EMBED_ICON.png"
    OPENWEATHERMAP_ICON = "https://somibot.skillp.dev/cdn/images/OPENWEATHERMAP_ICON.png"
    SOMI_BEST_GRILL_IMAGE = "https://somibot.skillp.dev/cdn/images/SOMI_BEST_GRILL_IMAGE.png"
    SPOTIFY_ICON = "https://somibot.skillp.dev/cdn/images/SPOTIFY_ICON.png"

    # SOMICORD
    SKILLP_JOINED_SOMICORD_TIME = 1573055760
    SOMICORD_ID = Config.MODMAIL_SERVER_ID
    SOMICORD_MOD_CHANNEL_ID = Config.MODMAIL_CHANNEL_ID
    SOMICORD_WELCOME_CHANNEL_ID = Config.WELCOME_CHANNEL_ID
    SOMICORD_WELCOME_GIF = "https://somibot.skillp.dev/cdn/gifs/SOMICORD_WELCOME_GIF.gif"

    # Emotes
    HEADS_EMOTE = Config.HEADS_EMOTE
    REACTION_EMOTE = Config.REACTION_EMOTE
    SOMI_BEST_GRILL_EMOTE = Config.SOMI_BEST_GRILL_EMOTE
    SOMI_F_EMOTE = Config.SOMI_F_EMOTE
    SOMI_ONLY_EMOTE = Config.SOMI_ONLY_EMOTE
    SOMI_WELCOME_EMOTE = Config.SOMI_WELCOME_EMOTE
    TAILS_EMOTE = Config.TAILS_EMOTE

    # Variables
    start_time = int(time.time())

    # Class imports
    Keychain = Keychain()
    Lists = Lists()
    Loggers = Loggers()

    ####################################################################################################

    def __init__(self) -> None:
        super().__init__(
            application_id = Config.APPLICATION_ID,
            intents = nextcord.Intents.all(),
            status = nextcord.Status.online,
            activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="Ice Cream"),
            allowed_mentions = nextcord.AllowedMentions(everyone=False),
            owner_id = Config.OWNER_ID
        )

    ####################################################################################################

    def api_login(self) -> None:
        """This function adds API logins from LastFm, Spotify, WolframAlpha and YouTube on the client"""

        self.lf_network = pylast.LastFMNetwork(
            api_key = Keychain().LAST_FM_API_KEY,
            api_secret = Keychain().LAST_FM_API_SECRET,
            username = Keychain().LAST_FM_USERNAME,
            password_hash = pylast.md5(Keychain().LAST_FM_PASSWORD)
        )

        self.spotifyOAuth = spotipy.SpotifyOAuth(
            client_id = Keychain().SPOTIPY_CLIENT_ID,
            client_secret = Keychain().SPOTIPY_CLIENT_SECRET,
            redirect_uri = Keychain().SPOTIPY_REDIRECT_URI,
            scope="user-read-currently-playing"
        )

        self.wolfram_client = wolframalpha.Client(self.Keychain.WOLFRAM_APP_ID)

        self.youtube = googleapiclient.discovery.build(
            'youtube',
            'v3',
            developerKey = self.Keychain.YOUTUBE_API_KEY
        )

    ####################################################################################################

    async def api_logout(self) -> None:
        """Logs the client from the Spotify and YouTube API out"""

        if hasattr(self, "spotifyOAuth"):
            self.spotifyOAuth._session.close()

        if hasattr(self, "youtube"):
            self.youtube.close()

    ####################################################################################################

    async def on_ready(self) -> None:
        """This function overwrites the build in on_ready function"""

        # logout in case this was a restart and we didn't properly exit those API connections
        await self.api_logout()
        self.Loggers.bot_status(f"{self.user}: ready and logged in")
        self.api_login()

        await self.start_infinite_loops()

    ####################################################################################################

    async def on_close(self) -> None:
        """This function overwrites the build in on_close function"""

        self.Loggers.bot_status(f"{self.user}: logged out")

        # attempt to logout the api connections
        try:
            if requests.get("https://www.google.com/").status_code == 200:
                await self.api_logout()
        except (requests.ConnectionError):
            pass

    ####################################################################################################

    async def on_disconnect(self) -> None:
        """This function overwrites the build in on_disconnect function"""

        self.Loggers.bot_status(f"{self.user}: connection closed")

        # attempt to logout the api connections
        try:
            if requests.get("https://www.google.com/").status_code == 200:
                await self.api_logout()
        except (requests.ConnectionError):
            pass

    ####################################################################################################

    async def start_infinite_loops(self) -> None:
        """This function starts an infinite loop for the ReminderSend cog, which continues until the bot loses internet or gets shutdown"""

        from cogs.reminder.ReminderSend import ReminderSend

        await asyncio.gather(ReminderSend(self).infinite_reminder_loop())

    ####################################################################################################

    async def on_member_join(self, member: nextcord.Member) -> nextcord.Message:
        """This function overwrites the build in on_member_join function"""

        await asyncio.gather(
            self.get_cog("JoinLog").join_log(member),
            self.get_cog("Welcome").welcome(member)
        )

    ####################################################################################################

    async def on_member_remove(self, member: nextcord.Member) -> nextcord.Message:
        """This function overwrites the build in on_member_remove function"""

        await asyncio.gather(
            self.get_cog("LeaveLog").leave_log(member)
        )

    ####################################################################################################

    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member) -> nextcord.Message:
        """This function overwrites the build in on_member_update function"""

        await asyncio.gather(
            self.get_cog("NameLog").name_log(before, after)
        )

    ####################################################################################################

    async def on_message(self, message: nextcord.Message) -> nextcord.Message:
        """This function overwrites the build in on_message function"""

        await asyncio.gather(
            self.get_cog("KeywordSend").keyword_send(message),
            self.get_cog("KeywordSend").levels_gain_xp(message),
            self.get_cog("LinkEmbed").link_embed(message),
            self.get_cog("Modmail").modmail(message),
            self.get_cog("Reactions").reaction(message)
        )

        return await super().on_message(message)
    
    ####################################################################################################

    async def on_message_delete(self, message: nextcord.Message) -> None:
        """This function overwrites the build in on_message_delete function"""

        await asyncio.gather(
            self.get_cog("DeleteLog").delete_log(message)
        )

    ####################################################################################################

    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message) -> None:
        """This function overwrites the build in on_message_edit function"""

        await asyncio.gather(
            self.get_cog("EditLog").edit_log(before, after)
        )


    ####################################################################################################

    @staticmethod
    async def on_application_command_completion(interaction: nextcord.Interaction) -> None:
        """This function overwrites the build in on_application_command_completion function, to update the usage count of a command with the name of the used application command"""

        commandname: str = ""

        if not hasattr(interaction, "application_command"):
            return

        if hasattr(interaction.application_command, "parent_cmd"):
            commandname += f"{interaction.application_command.parent_cmd.name}"

        if hasattr(interaction.application_command, "name"):
            commandname += f" {interaction.application_command.name}"

        if commandname:
            CommandUsesDB("command_uses").update(f"{commandname}")

    ####################################################################################################

    async def on_application_command_error(
        self,
        interaction: nextcord.Interaction,
        exception: nextcord.ApplicationError
    ) -> tuple[nextcord.Interaction, nextcord.ApplicationError]:
        """This function overwrites the build in on_application_command_error function, to create a global error log and exception handler."""

        from lib.modules.EmbedFunctions import EmbedFunctions
        from lib.modules.Get import Get

        if not hasattr(interaction, "channel"):
            return

        self.Loggers.application_command_error(
            exception = exception,
            type = interaction.type._name_,
            file = interaction.application_command.parent_cog,
            meta_data = Get().log_message(interaction, "error"),
            data = interaction.data,
            app_permissions = interaction.app_permissions.value,
            permissions = interaction.permissions.value,
        )

        ERROR_MESSAGE = f"An error has occured while executing this command, make sure {self.user.mention} has all the required permissions.\nIf this persits you can file a bug-report by using `/feedback`."

        if interaction.response.is_done():
            await interaction.followup.send(embed=EmbedFunctions().critical_error(ERROR_MESSAGE), ephemeral=True)
        else:
            await interaction.response.send_message(embed=EmbedFunctions().critical_error(ERROR_MESSAGE), ephemeral=True)

        return await super().on_application_command_error(interaction, exception)

    ####################################################################################################

    async def on_thread_join(self, thread: nextcord.Thread):
        """This function overwrites the build in on_thread_join so that the client automatically joins all new threads."""

        try:
            await thread.join()
        except:
            pass

    ####################################################################################################

    @staticmethod
    def restart() -> None:
        """This function will restart the bot, by closing and reopening the main file"""

        os.execv(sys.executable, ['python'] + sys.argv)

    ####################################################################################################

    @staticmethod
    async def deactivate_view_children(ButtonClass: nextcord.ui.View) -> None:
        """This function deactivates all children from a view (buttons/select boxes)"""

        # disable all buttons from this view
        for child in ButtonClass.children:
            child.disabled = True
            
        response: nextcord.Message = getattr(ButtonClass, "response", None)
        interaction: nextcord.Interaction = getattr(ButtonClass, "interaction", None)
        
        # edit the original class to have its buttons deactivated
        if response:
            await response.edit(view=ButtonClass)
        elif interaction:
            await interaction.edit_original_message(view=ButtonClass)