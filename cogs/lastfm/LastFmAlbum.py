from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import urllib.parse

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get, Webscrape
from lib.utilities import Lists, SomiBot



class LastFmAlbum(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "album", description = "shows you your LastFm stats for any album")
    async def lastfm_album(
        self,
        interaction: nextcord.Interaction,
        *,
        artist: str = nextcord.SlashOption(
            description = "the artist you want to see your stats for",
            required = False,
            min_length = 2,
            max_length = 100
        ),
        album: str = nextcord.SlashOption(
            description = "the album you want to see your stats for",
            required = False,
            min_length = 2,
            max_length = 100
        ),
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want to be shown, what they're listening to",
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            description = "the timeframe you want the top tracks for",
            required = False,
            choices = Lists.LASTFM_TIMEFRAMES_WEBSCRAPING
        )
    ) -> None:
        """This command webscrapes the data of a user from LastFm to get their top tracks for a certain album"""

        # if only one of artist and album was provided error
        if (not artist and album) or (artist and not album):
            await interaction.response.send_message(embed=EmbedFunctions().error(f"Please name both an artist and an album."), ephemeral=True)
            return

        if not user:
            user = interaction.user

        if not timeframe:
            timeframe = "ALL"

        lastfm_username = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_get()

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if not artist and not album:
            np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

            if np_response.status_code != 200:
                await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            # get the artist and album they're listening to/last listened to from the recent tracks
            np_user_data = np_response.json()
            artist =  np_user_data["recenttracks"]["track"][0]['artist']['#text']
            album = np_user_data["recenttracks"]["track"][0]['album']['#text']

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf album",
            {"artist": artist, "album": album, "user": str(user.id), "timeframe": timeframe}
        ))


        artist_for_url = urllib.parse.quote_plus(artist)
        album_for_url = urllib.parse.quote_plus(album)
        album_response = requests.get(
            f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/{album_for_url}?date_preset={timeframe}",
            cookies=self.client.Keychain.LAST_FM_COOKIES,
            headers=self.client.Keychain.LAST_FM_HEADERS
        )

        if album_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().error(f"The album `{artist}` - `{album}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(album_response.content, "html.parser")

        if "didn't scrobble this album during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().error(f"{user.mention} hasn't listened to the album `{artist}` - `{album}` in the timeframe: `{Lists.LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, artist_name, cover_image_url, metadata_list, track_output, _ = Webscrape().library_subpage(soup, artist_for_url, "album")

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{user.display_name} × {type_name}: {Lists.LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/{album_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"by [{artist_name}](https://www.last.fm/music/{artist_for_url})\n\n" +
                          f"**Top Tracks**\n" +
                          f"{track_output}\n",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)


def setup(client: SomiBot) -> None:
    client.add_cog(LastFmAlbum(client))
