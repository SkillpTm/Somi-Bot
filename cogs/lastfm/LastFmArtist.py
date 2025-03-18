from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import urllib.parse

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get, Webscrape
from lib.utilities import Lists, SomiBot



class LastFmArtist(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(name = "artist", description = "shows you your LastFm stats for any artist")
    async def lastfm_artist(
        self,
        interaction: nextcord.Interaction,
        *,
        artist: str = nextcord.SlashOption(
            description = "the artist you want to see your stats for",
            required = False,
            min_length = 2,
            max_length = 100
        ),
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want to be shown, what they're listening to",
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            description = "the timeframe you want the top albums for",
            required = False,
            choices = Lists.LASTFM_TIMEFRAMES_WEBSCRAPING
        )
    ) -> None:
        """This command webscrapes the data of a user from LastFm to get their top tracks and top albums for a certain artist"""

        if not user:
            user = interaction.user

        if not timeframe:
            timeframe = "ALL"

        lastfm_username = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_get()

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if not artist:
            np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

            if np_response.status_code != 200:
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            # get the artist they're listening to/last listened to from the recent tracks
            artist =  np_response.json()["recenttracks"]["track"][0]['artist']['#text']

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf artist",
            {"artist": artist, "user": str(user.id), "timeframe": timeframe}
        ))


        artist_for_url = urllib.parse.quote_plus(artist)
        artist_response = requests.get(f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}", cookies=self.client.Keychain.LAST_FM_COOKIES, headers=self.client.Keychain.LAST_FM_HEADERS)

        if artist_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"The artist `{artist}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(artist_response.content, "html.parser")

        if "didn't scrobble any albums by this artist during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{user.mention} hasn't listened to the artist `{artist}` in the timeframe: `{Lists.LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, _, cover_image_url, metadata_list, track_output, album_output = Webscrape().library_subpage(soup, artist_for_url, "artist")

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{user.display_name} × {type_name}: {Lists.LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"Listened to: **{metadata_list[1]}** Albums // **{metadata_list[2]}** Tracks\n\n" +
                          f"**Top Albums**\n" +
                          f"{album_output}\n" +
                          f"**Top Tracks**\n" +
                          f"{track_output}\n",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)


def setup(client: SomiBot) -> None:
    client.add_cog(LastFmArtist(client))
