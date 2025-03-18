import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import urllib.parse

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import PageButtons, SomiBot



class LastFmRecent(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(name = "rc", description = "shows your recently played songs on LastFm", name_localizations = {country_tag:"recent" for country_tag in nextcord.Locale})
    async def lastfm_recent(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want the recent tracks of",
            required = False
        )
    ) -> None:
        """This command shows someone's recent tracks and what they are now playing on the first page"""

        if not user:
            user = interaction.user

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf recent",
            {"user": str(user.id)}
        ))

        lastfm_username = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_get()

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        # send a dummy respone to be updated in the recursive function
        await interaction.response.send_message(embed=EmbedFunctions().builder(title=" "))

        await self.lastfm_recent_rec(interaction, user, lastfm_username, page_number = 1, first_message_sent = False)

    ####################################################################################################

    async def lastfm_recent_rec(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.User,
        lastfm_username: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=10&page={page_number}&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if np_response.status_code != 200:
            await interaction.edit_original_message(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"), view=None) 
            return

        np_data = np_response.json()
        last_page = int(np_data["recenttracks"]["@attr"]["totalPages"])
        output = ""
        index = 0

        # formats the last 10 songs as following in a string:
        # 1. [song name](song link) by [artist](artist link) - timestamp
        for track in np_data["recenttracks"]["track"]:
            index += 1
            track_url = track['url']
            artist_name_for_url = urllib.parse.quote_plus(track['artist']['#text'])

            track_name = Get.markdown_safe(track['name'])
            artist_name = Get.markdown_safe(track['artist']['#text'])
            timestamp = ""

            # set the timestamp, unless it is currently playing
            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
            else:
                index -= 1
                if page_number == 1:
                    timestamp = "*now playing*"

            if timestamp != "":
                output += f"{index + (page_number - 1) * 10}. **[{track_name}]({track_url})** by [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            author = f"{user.display_name} recently played:",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        view = PageButtons(page = page_number, last_page = last_page, interaction = interaction)

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_recent_rec(interaction, user, lastfm_username, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmRecent(client))