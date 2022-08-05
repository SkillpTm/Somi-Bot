###package#import###############################################################################

import lyricsgenius
import nextcord
from nextcord import Embed, Interaction, SlashOption, Spotify
from nextcord.ext import commands
import os
import string
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import GENIUS_COLOR, GENIUS_ICON



class lyrics(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###lyrics###########################################################

    @nextcord.slash_command(name='lyrics', description='Posts the lyircs to the song you are playing')
    async def spotify(self,
                      interaction: Interaction,
                      *,
                      artist: str = SlashOption(description="The artist you want a song to see the lyrics of", required=False),
                      song: str = SlashOption(description="The song of that artist you want the lyrics of", required=False)):
        if not checks(interaction):
            return

        if artist == None and song == None:
            member = interaction.guild.get_member(interaction.user.id)

            for activity in member.activities:
                if isinstance(activity, Spotify):
                    artist = str(activity.artist)
                    song = str(activity.title)

        if artist == None or song == None:
            await interaction.response.send_message("Please select a valid artist **and** a valid song or play a song on Spotify!", ephemeral=True)
            return
        
        access_token = os.environ['GENIUS_ACCESS_TOKEN']
        genius = lyricsgenius.Genius(access_token)

        genius_song = genius.search_song(title=song, artist=artist)

        try:
            genius_song_lyrics = genius_song.lyrics[:-5] #Get rid of an error in the wrapper
            
            if genius_song_lyrics[len(genius_song_lyrics)-1] in str(string.digits):
                genius_song_lyrics = genius_song_lyrics[:-1] #Get rid of another error in the wrapper

            genius_song_url = genius_song.url
        except:
            await interaction.response.send_message("The Genius search failed, please search with different criteria again!", ephemeral=True)
            return

        embed = Embed(title = f"{genius_song.title}",
                      url = genius_song_url,
                      description = genius_song_lyrics[:4096],
                      colour=GENIUS_COLOR)
        try:
            embed.set_thumbnail(url = genius_song.header_image_thumbnail_url)
        except:
            pass
        
        embed.set_author(name= f"{genius_song.artist}", icon_url=GENIUS_ICON)
        embed.set_footer(text = "Lyrics powered by Genius")

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "lyrics")

def setup(client):
    client.add_cog(lyrics(client))