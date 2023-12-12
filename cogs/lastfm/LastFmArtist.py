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

        artist_name, cover_image, artist_stats, album_output, track_output = self.webscrape_artist_page(soup, artist_for_url)

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image,
            author = f"{member.display_name} X {artist_name.text}: {LASTFM_TIMEFRAMES_ARTIST_TEXT[timeframe]}",
            author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
            author_icon = self.client.LASTFM_ICON,
            description = f"Total plays: __**{artist_stats[0]}**__\n" +
                          f"Listened to: **{artist_stats[1]}** Albums // **{artist_stats[2]}** Tracks\n\n" +
                          f"**Top Albums**\n" +
                          f"{album_output}\n" +
                          f"**Top Tracks**\n" +
                          f"{track_output}\n",
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)

    ####################################################################################################

    @staticmethod
    def webscrape_artist_page(soup, artist_for_url):
        """This function webscrapes the artist page of a given user"""

        artist_name: str = soup.find("h2", class_="library-header-title") # Artist name

        results_image = soup.find("span", class_="avatar library-header-image")
        cover_image: str = results_image.img["src"] # Artist iamge

        results_stats = soup.find_all("p", class_="metadata-display")
        artist_stats = [stat.text for stat in results_stats] # (Scrobbles, Albums, Tracks) amount

        results_albums_and_tracks = soup.find_all("tbody")
        album_output = "" # index_number, album with url - scrobble amount
        track_output = "" # index_number, track with url - scrobble amount
        i=0

        # this html structure should always appear, all other scenarios got fail saved
        for tablebody in results_albums_and_tracks:
            i+=1
            # i=2 -> working on album
            # i=4 -> working on track
            if i == 5:
                break
            if not i % 2 == 0:
                continue
            for tr in tablebody:
                for td in tr:
                    # index_number
                    if 'chartlist-index' in str(td): # unique class name of the td needed
                        position = re.sub('\n', '', td.text)
                        position = re.sub(' ', '', position)

                        if i == 2:
                            album_output += f"{position}. " # Album/track Spot
                        elif i == 4:
                            track_output += f"{position}. " # Album/track Spot

                    # album/track with url    
                    if 'chartlist-name' in str(td): # unique class name of the td needed
                        name = Get().markdown_safe(re.sub('\n', '', td.text)) # can be both album and track

                        name_for_url = re.sub('\n', '', td.text)
                        name_for_url = urllib.parse.quote_plus(name_for_url)

                        if i == 2:
                            album_output += f"[{name}](https://www.last.fm/music/{artist_for_url}/{name_for_url}/) " # URL and album name
                        elif i == 4:
                            track_output += f"[{name}](https://www.last.fm/music/{artist_for_url}/_/{name_for_url}/) " # URL and track name

                    # scrobble amount
                    if 'chartlist-count-bar' in str(td): # unique class name of the td needed
                        for span1 in td:
                            for a in span1:
                                for span2 in a:
                                    if "chartlist-count-bar-value" in str(span2): # unique class name of the span needed
                                        scorbble_amount = re.sub('\n', '', span2.text)
                                        scorbble_amount = re.sub(' ', '', scorbble_amount)
                                        SCROBBLE_REPLACMENTS = {
                                            "scrobbles": "plays",
                                            "scrobble": "play"
                                        }

                                        for key, value in SCROBBLE_REPLACMENTS.items():
                                            scorbble_amount = scorbble_amount.replace(key, f" {value}") # has to be done after re.sub, to keep that space before plays

                                        if i == 2:
                                            album_output += f"- *({scorbble_amount})*\n" # Scrobble amount for album/track
                                        elif i == 4:
                                            track_output += f"- *({scorbble_amount})*\n"# Scrobble amount for album/track

        return artist_name, cover_image, artist_stats, album_output, track_output



def setup(client: SomiBot):
    client.add_cog(LastFmArtist(client))
