####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import urllib.parse

####################################################################################################

from lib.modules import Checks, EmbedFunctions, Webscrape
from lib.utilities import SomiBot



class Lyrics(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name='genius', description='Posts the lyircs to the song you are playing', name_localizations = {country_tag:"lyrics" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lyrics(self,
                      interaction: nextcord.Interaction,
                      *,
                      artist: str = nextcord.SlashOption(description="the artist you want a song to see the lyrics of", required=False, min_length=2, max_length=100),
                      song: str = nextcord.SlashOption(description="the song of that artist you want the lyrics of", required=False, min_length=2, max_length=100)):
        """This command will post the lyrics of a song in an embed, through the slashh options or by pulling it from their Spotify connection with Discord"""

        if not artist and not song:
            member: nextcord.Member = interaction.guild.get_member(interaction.user.id)

            for activity in member.activities:
                if not isinstance(activity, nextcord.Spotify):
                    continue
                
                artist = activity.artist
                song = activity.title

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lyrics {artist} - {song}")

        if not artist or not song:
            await interaction.response.send_message(embed=EmbedFunctions().error("Please select a valid artist **and** a valid song or play a song on Spotify!"), ephemeral=True)
            return

        headers = {"Authorization": f"Bearer {self.client.Keychain.GENIUS_ACCESS_TOKEN}"}
        artist_song = urllib.parse.quote_plus(f"{artist}+{song}")
        search_response = requests.get(f"https://api.genius.com/search?q={artist_song}", headers=headers).json()

        if not search_response["response"]["hits"] or search_response["response"]["hits"][0]["type"] != "song":
            await interaction.response.send_message(embed=EmbedFunctions().error("Please select a valid artist **and** a valid song or play a song on Spotify!"), ephemeral=True)
            return
        
        await interaction.response.defer(with_message=True)
        
        song_url = search_response["response"]["hits"][0]["result"]["url"]

        lyrics_text = Webscrape().genius_lyrics(song_url)

        if not lyrics_text:
            await interaction.followup.send(embed=EmbedFunctions().error(f"Your search for:\nArtist: `{artist}`\nSong: `{song}`\n__failed__, please try again!"))
            return
        
        song_response = requests.get(f"https://api.genius.com/songs/{search_response["response"]["hits"][0]["result"]["id"]}", headers=headers).json()


        embed = EmbedFunctions().builder(
            color = self.client.GENIUS_COLOR,
            thumbnail = song_response["response"]["song"]["song_art_image_url"],
            author = song_response["response"]["song"]["title"],
            author_icon = self.client.GENIUS_ICON,
            author_url = song_url,
            description = lyrics_text,
            footer = "Lyrics powered by Genius"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Lyrics(client))