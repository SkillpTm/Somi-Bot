import urllib.parse

from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions, Webscrape
from lib.managers import Commands, Config, Keychain, Lists
from lib.modules import SomiBot



class LastFmTrack(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(Commands().data["lf track"].name, Commands().data["lf track"].description)
    async def lastfm_track(
        self,
        interaction: nextcord.Interaction,
        *,
        artist: str = nextcord.SlashOption(
            Commands().data["lf track"].parameters["artist"].name,
            Commands().data["lf track"].parameters["artist"].description,
            required = False,
            min_length = 2,
            max_length = 100
        ),
        track: str = nextcord.SlashOption(
            Commands().data["lf track"].parameters["track"].name,
            Commands().data["lf track"].parameters["track"].description,
            required = False,
            min_length = 2,
            max_length = 100
        ),
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf track"].parameters["user"].name,
            Commands().data["lf track"].parameters["user"].description,
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            Commands().data["lf track"].parameters["timeframe"].name,
            Commands().data["lf track"].parameters["timeframe"].description,
            required = False,
            choices = Lists().LASTFM_TIMEFRAMES_WEBSCRAPING
        )
    ) -> None:
        """This command webscrapes the data of a user from LastFm to get their plays on a track"""

        # if only one of artist and track was provided error
        if (not artist and track) or (artist and not track):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please name both an artist and a track."), ephemeral=True)
            return

        user = user or interaction.user
        timeframe = timeframe or "ALL"

        if not (lastfm_username := await db.User.LASTFM.get(interaction.user.id)):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        if not artist and not track:
            np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

            if np_response.status_code != 200:
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            np_user_data = np_response.json()
            artist =  np_user_data["recenttracks"]["track"][0]["artist"]["#text"]
            track = np_user_data["recenttracks"]["track"][0]["name"]


        artist_for_url = urllib.parse.quote_plus(artist)
        track_for_url = urllib.parse.quote_plus(track)
        track_response = requests.get(
            f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}",
            cookies = Keychain().LAST_FM_COOKIES,
            headers = Keychain().LAST_FM_HEADERS,
            timeout = 10
        )

        if track_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"The track `{artist} - {track}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(track_response.content, "html.parser")

        if "didn't scrobble this track during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{user.mention} hasn't listened to the track `{artist} - {track}` in the timeframe: `{Lists().LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, artist_name, cover_image_url, metadata_list, _, _ = Webscrape().library_subpage(soup, artist_for_url, "track")

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{user.display_name} × {type_name}: {Lists().LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}",
            author_icon = Config().LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"[{type_name}](https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}) by [{artist_name}](https://www.last.fm/music/{artist_for_url})"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTrack(client))