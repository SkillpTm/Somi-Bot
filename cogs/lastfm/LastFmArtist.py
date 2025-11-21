import urllib.parse

from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions, Get, Webscrape
from lib.managers import Commands, Config, Keychain, Lists
from lib.modules import SomiBot



class LastFmArtist(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(Commands().data["lf artist"].name, Commands().data["lf artist"].description)
    async def lastfm_artist(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        artist: str = nextcord.SlashOption(
            Commands().data["lf artist"].parameters["artist"].name,
            Commands().data["lf artist"].parameters["artist"].description,
            required = False,
            min_length = 2,
            max_length = 100
        ),
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf artist"].parameters["user"].name,
            Commands().data["lf artist"].parameters["user"].description,
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            Commands().data["lf artist"].parameters["timeframe"].name,
            Commands().data["lf artist"].parameters["timeframe"].description,
            required = False,
            choices = Lists().LASTFM_TIMEFRAMES_WEBSCRAPING
        )
    ) -> None:
        """This command webscrapes the data of a user from LastFm to get their top tracks and top albums for a certain artist"""

        user = user or interaction.user
        timeframe = timeframe or Lists().LASTFM_TIMEFRAMES_WEBSCRAPING["All Time"]

        if not (lastfm_username := str(await db.User.LASTFM.get(interaction.user.id) or "")):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        if not artist:
            np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

            if np_response.status_code != 200:
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            # get the artist they're listening to/last listened to from the recent tracks
            artist =  np_response.json()["recenttracks"]["track"][0]["artist"]["#text"]


        artist_for_url = urllib.parse.quote_plus(artist)
        artist_response = requests.get(
            f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
            cookies = Keychain().LAST_FM_COOKIES, # type: ignore
            headers = Keychain().LAST_FM_HEADERS, # type: ignore
            timeout = 10
        )

        if artist_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"The artist `{artist}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(artist_response.content, "html.parser")

        if "didn't scrobble any albums by this artist during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{user.mention} hasn't listened to the artist `{artist}` in the timeframe: `{Lists().LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, _, cover_image_url, metadata_list, track_output, album_output = Webscrape().library_subpage(soup, artist_for_url, "artist")
        footer = ""

        if (scrobbles_this_month := Get.lf_scrobbles_this_month(lastfm_username)) is not None:
            footer = f"{scrobbles_this_month} scrobbles in the last 30 days"

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{user.display_name} × {type_name}: {Lists().LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
            author_icon = Config().LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"Listened to: **{metadata_list[1]}** Albums // **{metadata_list[2]}** Tracks\n\n" +
                          "**Top Albums**\n" +
                          f"{album_output}\n" +
                          "**Top Tracks**\n" +
                          f"{track_output}\n",
            footer = footer,
            footer_icon = Config().HEADPHONES_ICON
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmArtist(client))