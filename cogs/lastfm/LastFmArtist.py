###package#import###############################################################################

import nextcord
import requests
import re
from bs4 import BeautifulSoup

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.GlobalData import network
from database.database_command_uses import uses_update
from database.database_lastfm import lastfm_get_user_from_db
from utilities.maincommands import checks
from utilities.variables import LASTFM_ICON, LASTFM_COLOR
from utilities.partial_commands import get_nick_else_name, embed_builder



class LastFmArtist(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#artist###########################################################

    @lastfm.subcommand(name = "artist", description = "shows you your LastFm stats for any artist")
    async def artist(self,
                     interaction: nextcord.Interaction,
                     *,
                     artist: str = nextcord.SlashOption(description="the artist you want to see your stats for", required=False, min_length=1, max_length=100),
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want to be shown, what they're listening to", required=False),
                     timeframe: str = nextcord.SlashOption(description="the timeframe you want the top albums for", required=False, choices = {"Past Week": "7day", "Past Month": "1month", "Past Quarter": "3month", "Past Half a Year": "6month", "Past Year": "12month", "All Time": "overall"})):
        if not checks(interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        if timeframe == None:
            timeframe = "overall"

        lastfm_username = lastfm_get_user_from_db(member.id)

        if not lastfm_username:
            await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
            return

        await interaction.response.defer(with_message = True)
        
        if artist == None:
            request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={network.api_key}&format=json")

            if not request_url.status_code == 200:
                await interaction.followup.send("LastFm didn't respond correctly, try in a few minutes again!")
                return

            np_user_data = request_url.json()
            artist =  np_user_data["recenttracks"]["track"][0]['artist']['#text']

        print(f"{interaction.user}: /lf artist {artist} {lastfm_username} {timeframe}")

        # WEBSCRAPING

        artist_for_url = artist.replace(" ", "+")
        page = requests.get(f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}")

        if not page.status_code == 200:
            await interaction.followup.send(f"The artist `{artist}` couldn't be found on LastFm.")
            return

        soup = BeautifulSoup(page.content, "html.parser")

        if "didn't scrobble any albums by this artist during the selected date range. Try expanding the date range or view scrobbles for " in str(soup.text):
            await interaction.followup.send(f"`{lastfm_username}` hasn't listened to the artist `{artist}` in the timeframe: `{timeframe}`")
            return

        artist_name = soup.find("h2", class_="library-header-title") # Artist name

        results_image = soup.find("span", class_="avatar library-header-image")
        cover_image = results_image.img["src"] # Artist iamge

        results_stats = soup.find_all("p", class_="metadata-display")
        artist_stats = [result.text for result in results_stats] # (Scrobbles, Albums, Tracks) amount

        results_albums_and_tracks = soup.find_all("tbody")
        album_output = "" # index_number, album with url - scrobble amount
        track_output = "" # index_number, track with url - scrobble amount
        i=0

        # this html structure should always appear, all other scenarios got fail saved
        for tablebody in results_albums_and_tracks:
            i+=1
            # i=1 -> working on album
            # i=2 -> working on track
            if i == 3:
                break
            for tr in tablebody:
                for td in tr:
                    # index_number
                    if 'chartlist-index' in str(td): # unique class name of the td needed
                        position = re.sub('\n', '', td.text)

                        if i == 1:
                            album_output += f"{position}. " # Album/track Spot
                        elif i == 2:
                            track_output += f"{position}. " # Album/track Spot

                    # album/track with url    
                    if 'chartlist-name' in str(td): # unique class name of the td needed
                        name = re.sub('\n', '', td.text) # can be both album and track
                        name_for_url = re.sub('\n', '', td.text)
                        name_for_url = re.sub(' ', '+', name_for_url)

                        if i == 1:
                            album_output += f"[{name}](https://www.last.fm/music/{artist_for_url}/{name_for_url}/) " # URL and album name
                        elif i == 2:
                            track_output += f"[{name}](https://www.last.fm/music/{artist_for_url}/_/{name_for_url}/) " # URL and track name

                    # scrobble amount
                    if 'chartlist-count-bar' in str(td): # unique class name of the td needed
                        for span1 in td:
                            for a in span1:
                                for span2 in a:
                                    if "chartlist-count-bar-value" in str(span2): # unique class name of the span needed
                                        scorbble_amount = re.sub('\n', '', span2.text)
                                        scorbble_amount = re.sub(' ', '', scorbble_amount)
                                        scorbble_amount = scorbble_amount.replace('scrobbles', ' plays') # has to be done after re.sub, to keep that space before plays

                                        if i == 1:
                                            album_output += f"- *({scorbble_amount})*\n" # Scrobble amount for album/track
                                        elif i == 2:
                                            track_output += f"- *({scorbble_amount})*\n"# Scrobble amount for album/track

        name = get_nick_else_name(member)
        authot_text_dict = {"7day": "of the past week:", "1month": "of the past month:", "3month": "of the past quarter:", "6month": "of the past half a year:", "12month": "of the past year:", "overall": "of all time:"}

        embed = embed_builder(description = f"""You have __**{artist_stats[0]}**__ scrobbles for this artist.
        You have played **{artist_stats[2]}** tracks on **{artist_stats[1]}** of their albums.
        
        **Top Albums**
        {album_output}
        **Top Tracks**
        {track_output}""",
                              color = LASTFM_COLOR,
                              thumbnail = cover_image,
                              author = f"{name} stats for {artist_name.text} {authot_text_dict[timeframe]}",
                              author_url = f"https://www.last.fm/user/{lastfm_username}/library/music/{artist_for_url}?date_preset={timeframe}",
                              author_icon = LASTFM_ICON,
                              footer = "DEFAULT_KST_FOOTER")

        await interaction.followup.send(embed=embed)

        uses_update("command_uses", "lf artist")



def setup(client):
    client.add_cog(LastFmArtist(client))