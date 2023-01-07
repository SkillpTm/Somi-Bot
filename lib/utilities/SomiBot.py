####################################################################################################

import asyncio
import asyncpraw
import nextcord
import nextcord.ext.commands as nextcord_C
import time
import pylast
import os
import requests
import spotipy
import sys

####################################################################################################

from lib.db_modules.CommandUsesDB import CommandUsesDB
from lib.utilities.Keychain import Keychain
from lib.utilities.Lists import Lists
from lib.utilities.Loggers import Loggers



class SomiBot(nextcord_C.Bot):

    #Meta
    SOMICORD_INVITE = "https://discord.gg/Frd7WYg"
    VERSION = "3.0"

    #Colors
    BOT_COLOR = 0xffa6fc
    GENIUS_COLOR = 0xf6f069
    LASTFM_COLOR = 0xd0232b
    MOD_COLOR = nextcord.Color.blue()
    REDDIT_COLOR = 0xfe4600

    #URLs
    BAN_HAMMER_GIF = "https://gfycat.com/bonygiddycoati"
    CLOCK_ICON = "https://i.imgur.com/nqDFTTP.png"
    GENIUS_ICON = "https://i.imgur.com/XF1cOBN.png"
    DEFAULT_PFP = "https://cdn.discordapp.com/embed/avatars/0.png"
    LASTFM_ICON = "https://i.imgur.com/a8QaskN.png"
    LINK_EMBED_ICON = "https://i.imgur.com/jgXT7if.png"
    OPENWEATHERMAP_ICON = "https://i.imgur.com/drJnhNn.png"
    REDDIT_ICON = "https://i.imgur.com/yXrvhM9.png"
    R_SOMI_DEFAULT_ICON = "https://i.imgur.com/HtTGMwc.gif"
    SOMI_BEST_GRILL_IMAGE = "https://i.imgur.com/65E2MWr.png"
    SPOTIFY_ICON = "https://i.imgur.com/YKtWQK4.png"

    #SOMICORD Constants
    REDDIT_FEED_ID = 1003709719447355512
    SKILLP_JOINED_SOMICORD_TIME = 1573055760
    SOMICORD_ID = 769668499605159998
    SOMICORD_ROLES_CHANNEL_ID = 981636345556512778
    SOMICORD_MOD_CHANNEL_ID = 992121127159726227
    SOMICORD_MODERATOR_ID = 977950744806297620
    SOMICORD_WELCOME_CHANNEL_ID = 847221019210809425
    SOMICORD_WELCOME_GIF = "https://cdn.discordapp.com/attachments/1057785281253744640/1057785437931974666/somi_welcome_gif.gif"

    #Emotes
    HEADS = "<:heads:998363203992031252>"
    REACTION_EMOTE = "<a:aSomiBreathTaking:980083399005982801>"
    SOMI_BEST_GRILL_EMOTE = "<:SomiBestGrill:924281555772403722>"
    SOMI_F_EMOTE = "<:SomiF:829933531147796510>"
    SOMI_ONLY_EMOTE = "<:SomiONLY:829934613509177354>"
    SOMI_WELCOME_EMOTE = "<a:aSomiWelcome:829917610765975552>"
    TAILS = "<:tails:998363225924046949>"

    #Variables
    start_time = int(time.time())

    #Class imports
    Keychain = Keychain()
    Lists = Lists()
    Loggers = Loggers()

    ####################################################################################################

    def __init__(self):
        super().__init__(
            application_id = 976963476771700786,
            intents = nextcord.Intents.all(),
            status = nextcord.Status.online,
            activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="XOXO - The First Album"),
            allowed_mentions = nextcord.AllowedMentions(everyone=False),
            owner_id = 378214190378123264
        )

    ####################################################################################################

    def api_login(self) -> None:
        """This function adds API logins from LastFm, Spotify and Reddit on to the client"""

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

        self.reddit = asyncpraw.Reddit(
            client_id = Keychain().REDDIT_ID,
            client_secret = Keychain().REDDIT_SECRET,
            username = "SomiBot",
            password = Keychain().REDDIT_PASSWORD,
            user_agent = "testscript by u/SkillpTm"
        )

    ####################################################################################################

    async def api_logout(self) -> None:
        """Logs the client from the Reddit and Spotify API out"""

        if hasattr(self, "reddit"):
            await self.reddit.close()

        if hasattr(self, "spotifyOAuth"):
            self.spotifyOAuth._session.close()

    ####################################################################################################

    async def on_ready(self) -> None:
        """This function overwrites the build in on_ready function"""

        from cogs.role_selection.RoleSelection import Roles, RoleSelection

        await RoleSelection(self).try_sending()
        self.add_view(Roles(self))

        self.Loggers.bot_status(f"Client {self.user} ready and logged in")
        print(f"Client {self.user} ready and logged in")

        self.api_login()

        await self.start_infinite_loops()

    ####################################################################################################

    async def on_resumed(self) -> None:
        """This function overwrites the build in on_resumed function"""

        self.Loggers.bot_status("Connection to Discord resumed")

        self.api_login()

        await self.start_infinite_loops()

    ####################################################################################################

    async def on_close(self) -> None:
        """This function overwrites the build in on_close function"""

        self.Loggers.bot_status(f"Logged out from {self.user}")

        try:
            requests.get("https://www.google.com/")
            await self.api_logout()
        except (requests.ConnectionError):
            pass

    ####################################################################################################

    async def on_disconnect(self) -> None:
        """This function overwrites the build in on_disconnect function"""

        self.Loggers.bot_status("Connection closed to Discord")

        try:
            requests.get("https://www.google.com/")
            await self.api_logout()
        except (requests.ConnectionError):
            pass

    ####################################################################################################

    async def start_infinite_loops(self) -> None:
        """This function starts an infinite loop for the Reddit and ReminderSend cog, which continues until the bot loses internet or gets shutdown"""

        from cogs.logs.Reddit import Reddit
        from cogs.reminders.ReminderSend import ReminderSend

        await asyncio.gather(Reddit(self).infinite_reddit_loop(), ReminderSend(self).infinite_reminder_loop())

    ####################################################################################################

    async def on_message(self,
                         message: nextcord.Message) -> nextcord.Message:
        """This function overwrites the build in on_message function"""

        if not message.guild in self.guilds and message.author.bot == False:
            return await super().on_message(message)

        if self.user.mentioned_in(message):
            await message.add_reaction(self.REACTION_EMOTE)

            self.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel:{message.channel.id} ~ User: {message.author.id} ~ reacted() @ping")

            CommandUsesDB().uses_update("log_activations", "reacted @ping")

        ####################################################################################################

        if "somionly" in str(message.content.lower()):
            await message.add_reaction(self.SOMI_ONLY_EMOTE)

            self.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel:{message.channel.id} ~ User: {message.author.id} ~ reacted() @SOMIONLY")

            CommandUsesDB().uses_update("log_activations", "reacted somionly")

        ####################################################################################################

        f_words = [" f ", self.SOMI_F_EMOTE.lower()]

        if any(i in f" {message.content.lower()} " for i in f_words):
            await message.add_reaction(self.SOMI_F_EMOTE)

            self.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel:{message.channel.id} ~ User: {message.author.id} ~ reacted() @SomiF")

            CommandUsesDB().uses_update("log_activations", "reacted SomiF")

        ####################################################################################################

        if "<:somibestgrill:924281555772403722>" in str(message.content.lower()):
            await message.add_reaction(self.SOMI_BEST_GRILL_EMOTE)

            self.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel:{message.channel.id} ~ User: {message.author.id} ~ reacted() @SomiBestGrill")

            CommandUsesDB().uses_update("log_activations", "reacted SomiBestGrill")

        return await super().on_message(message)

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

        if commandname != "":
            CommandUsesDB().uses_update("command_uses", f"{commandname}")

    ####################################################################################################

    async def on_application_command_error(self,
                                           interaction: nextcord.Interaction,
                                           exception: nextcord.ApplicationError) -> tuple[nextcord.Interaction, nextcord.ApplicationError]:
        """This function overwrites the build in on_application_command_completion function, to create a global error log and exception handler."""
        from lib.modules.EmbedFunctions import EmbedFunctions

        if not hasattr(interaction, "channel"):
            return

        self.Loggers.application_command_error(
            exception = exception,
            type = interaction.type._name_,
            file = interaction.application_command.parent_cog,
            meta_data = f"Guild = {interaction.guild.id} ~ Channel = {interaction.channel.id} ~ User = {interaction.user.id}",
            data = interaction.data,
            app_permissions = interaction.app_permissions.value,
            permissions = interaction.permissions.value,
        )

        ERROR_MESSAGE = f"An error has occured while executing this command, make sure {self.user.mention} has all the required permissions.\nIf this persits you can file a bug-report by using `/feedback`."

        if interaction.response.is_done():
            await interaction.followup.send(embed=EmbedFunctions().critical_error(ERROR_MESSAGE), ephemeral=True)

        else:
            try:
                await interaction.response.send_message(embed=EmbedFunctions().critical_error(ERROR_MESSAGE), ephemeral=True)
            except nextcord.errors.HTTPException:
                await interaction.followup.send(embed=EmbedFunctions().critical_error(ERROR_MESSAGE), ephemeral=True)

        return await super().on_application_command_error(interaction, exception)

    ####################################################################################################

    async def on_thread_join(self,
                             thread: nextcord.Thread):
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

        for child in ButtonClass.children:
            child.disabled = True
            
        response: nextcord.Message = getattr(ButtonClass, "response", None)
        interaction: nextcord.Interaction = getattr(ButtonClass, "interaction", None)
        
        if response != None:
            await response.edit(view=ButtonClass)
        elif interaction != None:
            await interaction.edit_original_message(view=ButtonClass)