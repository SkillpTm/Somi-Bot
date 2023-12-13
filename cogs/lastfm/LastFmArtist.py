####################################################################################################

from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import re
import urllib.parse

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import LASTFM_TIMEFRAMES_ARTIST, LASTFM_TIMEFRAMES_ARTIST_TEXT, LASTFM_COOKIES, LASTFM_HEADERS, SomiBot



class LastFmArtist(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "artist", description = "shows you your LastFm stats for any artist")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_artist(self,
                            interaction: nextcord.Interaction,
                            *,
                            artist: str = nextcord.SlashOption(description="the artist you want to see your stats for", required=False, min_length=2, max_length=100),
                            member: nextcord.Member = nextcord.SlashOption(description="the user you want to be shown, what they're listening to", required=False),
                            timeframe: str = nextcord.SlashOption(description="the timeframe you want the top albums for", required=False, choices=LASTFM_TIMEFRAMES_ARTIST)):
        """This command webscrapes the data of a user from LastFm to get their top tracks and top albums for a certain artist"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        if not timeframe:
            timeframe = "ALL"

        lastfm_username = LastFmDB().get_user(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if not artist:
            request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.lf_network.api_key}&format=json")

            if not request_url.status_code == 200:
                await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
                return

            np_user_data = request_url.json()
            artist =  np_user_data["recenttracks"]["track"][0]['artist']['#text']

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf artist {artist} {member.id} {timeframe}")


        artist_for_url = urllib.parse.quote_plus(artist)
        page = requests.get(f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}", cookies=LASTFM_COOKIES, headers=LASTFM_HEADERS)

        if not page.status_code == 200:
            await interaction.followup.send(embed=EmbedFunctions().error(f"The artist `{artist}` couldn't be found on LastFm."))
            return

        soup = BeautifulSoup(page.content, "html.parser")

        if "didn't scrobble any albums by this artist during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(embed=EmbedFunctions().error(f"{member.mention} hasn't listened to the artist `{artist}` in the timeframe: `{LASTFM_TIMEFRAMES_ARTIST_TEXT[timeframe]}`"))
            return

        artist_name, artist_image_url, artist_metadata, album_output, track_output = self.webscrape_artist_page(soup, artist_for_url)

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = artist_image_url,
            author = f"{member.display_name} X {artist_name.text}: {LASTFM_TIMEFRAMES_ARTIST_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{artist_metadata[0]}**__\n" +
                          f"Listened to: **{artist_metadata[1]}** Albums // **{artist_metadata[2]}** Tracks\n\n" +
                          f"**Top Albums**\n" +
                          f"{album_output}\n" +
                          f"**Top Tracks**\n" +
                          f"{track_output}\n",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)

    ####################################################################################################

    @staticmethod
    def webscrape_artist_page(soup: BeautifulSoup, artist_for_url: str) -> tuple[str, str, list[str], str, str]:
        """This function webscrapes the artist page of a given user"""

        artist_name: str = str(soup.find("h2", class_="library-header-title").text)

        found_image = soup.find("span", class_="avatar library-header-image")
        artist_image_url: str = str(found_image.img["src"])

        found_metadata = soup.find_all("p", class_="metadata-display")
        artist_metadata = [str(metadata.text) for metadata in found_metadata] # [Scrobbles, Albums, Tracks]

        found_positions = soup.find_all("td", class_="chartlist-index")
        positions_list = [str(position.text).replace(" ", "").replace("\n", "") for position in found_positions]

        found_names = soup.find_all("td", class_="chartlist-name")
        names_list = [str(name.text) for name in found_names if str(name.text).replace("\n", "")]

        found_scorbbles = soup.find_all("span", class_="chartlist-count-bar-value")
        scorbbles_list = [re.sub(r"[^\d]", "", scrobbles.text) for scrobbles in found_scorbbles]

        album_output = ""
        track_output = ""
        current_element_album = 0

        for position, name, scrobbles in zip(positions_list, names_list, scorbbles_list):
            if int(position) == 1:
                current_element_album += 1 # setting a flag for if we're working on albums or tracks

            name = re.sub('\n', '', name) # can be both album and track

            safe_name = Get().markdown_safe(name)

            name_for_url = urllib.parse.quote_plus(name)


            if int(scrobbles) == 1:
                scrobbles += " play"
            else:
                scrobbles += " plays"


            if current_element_album == 1:
                album_output += f"{position}. "
                album_output += f"[{safe_name}](https://www.last.fm/music/{artist_for_url}/{name_for_url}/ "
                album_output += f"- *({scrobbles})*\n"
            else:
                track_output += f"{position}. "
                track_output += f"[{safe_name}](https://www.last.fm/music/{artist_for_url}/_/{name_for_url}/ "
                track_output += f"- *({scrobbles})*\n"
        
        return artist_name, artist_image_url, artist_metadata, album_output, track_output



def setup(client: SomiBot):
    client.add_cog(LastFmArtist(client))
