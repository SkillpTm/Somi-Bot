from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import urllib.parse

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get, Webscrape
from lib.utilities import LASTFM_TIMEFRAMES_WEBSCRAPING, LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT, SomiBot



class LastFmTrack(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "track", description = "shows you your LastFm stats for any track")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def lastfm_track(
        self,
        interaction: nextcord.Interaction,
        *,
        artist: str = nextcord.SlashOption(
            description="the artist you want to see your stats for",
            required=False,
            min_length=2,
            max_length=100
        ),
        track: str = nextcord.SlashOption(
            description="the track you want to see your stats for",
            required=False,
            min_length=2,
            max_length=100
        ),
        user: nextcord.User = nextcord.SlashOption(
            description="the user you want to be shown, what they're listening to",
            required=False
        ),
        timeframe: str = nextcord.SlashOption(
            description="the timeframe you want the stats for",
            required=False,
            choices=LASTFM_TIMEFRAMES_WEBSCRAPING
        )
    ) -> None:
        """This command webscrapes the data of a user from LastFm to get their plays on a track"""

        # if only one of artist and track was provided error
        if (not artist and track) or (artist and not track):
            await interaction.response.send_message(embed=EmbedFunctions().error(f"Please name both an artist and a track."), ephemeral=True)
            return

        if not user:
            user = interaction.user

        if not timeframe:
            timeframe = "ALL"

        lastfm_username = LastFmDB().get(user.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if not artist and not track:
            np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.lf_network.api_key}&format=json")

            if np_response.status_code != 200:
                await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            np_user_data = np_response.json()
            artist =  np_user_data["recenttracks"]["track"][0]['artist']['#text']
            track = np_user_data["recenttracks"]["track"][0]['name']

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/lf track",
            {"artist": artist, "track": track, "user": str(user.id), "timeframe": timeframe}
        ))


        artist_for_url = urllib.parse.quote_plus(artist)
        track_for_url = urllib.parse.quote_plus(track)
        track_response = requests.get(f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}", cookies=self.client.Keychain.LAST_FM_COOKIES, headers=self.client.Keychain.LAST_FM_HEADERS)

        if track_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().error(f"The track `{artist} - {track}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(track_response.content, "html.parser")

        if "didn't scrobble this track during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().error(f"{user.mention} hasn't listened to the track `{artist} - {track}` in the timeframe: `{LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, artist_name, cover_image_url, metadata_list, _, _ = Webscrape().library_subpage(soup, artist_for_url, "track")

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{user.display_name} × {type_name}: {LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"[{type_name}](https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}) by [{artist_name}](https://www.last.fm/music/{artist_for_url})",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)


def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTrack(client))
