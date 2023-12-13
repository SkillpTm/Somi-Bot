####################################################################################################

from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import urllib.parse

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Webscrape
from lib.utilities import LASTFM_TIMEFRAMES_WEBSCRAPING, LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT, LASTFM_COOKIES, LASTFM_HEADERS, SomiBot



class LastFmTrack(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "track", description = "shows you your LastFm stats for any track")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_track(self,
                           interaction: nextcord.Interaction,
                           *,
                           artist: str = nextcord.SlashOption(description="the artist you want to see your stats for", required=False, min_length=2, max_length=100),
                           track: str = nextcord.SlashOption(description="the track you want to see your stats for", required=False, min_length=2, max_length=100),
                           member: nextcord.Member = nextcord.SlashOption(description="the user you want to be shown, what they're listening to", required=False),
                           timeframe: str = nextcord.SlashOption(description="the timeframe you want the stats for", required=False, choices=LASTFM_TIMEFRAMES_WEBSCRAPING)):
        """This command webscrapes the data of a user from LastFm to get their plays on a track"""

        if artist and track or not artist and not track:
            pass
        else:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"Please name both an artist and a track or neither, not just one."), ephemeral=True)
            return

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        if not timeframe:
            timeframe = "ALL"

        lastfm_username = LastFmDB().get_user(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if not artist and not track:
            request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.lf_network.api_key}&format=json")

            if not request_url.status_code == 200:
                await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            np_user_data = request_url.json()
            artist =  np_user_data["recenttracks"]["track"][0]['artist']['#text']
            track = np_user_data["recenttracks"]["track"][0]['name']

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf track {artist} {track} {member.id} {timeframe}")


        artist_for_url = urllib.parse.quote_plus(artist)
        track_for_url = urllib.parse.quote_plus(track)
        page = requests.get(f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}", cookies=LASTFM_COOKIES, headers=LASTFM_HEADERS)

        if not page.status_code == 200:
            await interaction.followup.send(embed=EmbedFunctions().error(f"The track `{artist} - {track}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(page.content, "html.parser")

        if "didn't scrobble this track during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().error(f"{member.mention} hasn't listened to the track `{artist} - {track}` in the timeframe: `{LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}`"))
            return

        type_name, artist_name, cover_image_url, metadata_list, track_output, album_output = Webscrape().library_subpage(soup, artist_for_url, "track")

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image_url,
            author = f"{member.display_name} X {type_name}: {LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}/_/{track_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{metadata_list[0]}**__\n" +
                          f"by [{artist_name}](https://www.last.fm/music/{artist_for_url})",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)


def setup(client: SomiBot):
    client.add_cog(LastFmTrack(client))
