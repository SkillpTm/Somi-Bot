###package#import###############################################################################

import lyricsgenius
import nextcord
from nextcord import Interaction, SlashOption, Spotify
from nextcord.ext import commands
import os
import string
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import GENIUS_COLOR, GENIUS_ICON



class lyrics(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###lyrics###########################################################

    @nextcord.slash_command(name='lyrics', description='Posts the lyircs to the song you are playing')
    async def lyrics(self,
                      interaction: Interaction,
                      *,
                      artist: str = SlashOption(description="The artist you want a song to see the lyrics of", required=False, min_length=1, max_length=100),
                      song: str = SlashOption(description="The song of that artist you want the lyrics of", required=False, min_length=1, max_length=100)):
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
        
        access_token = os.environ["GENIUS_ACCESS_TOKEN"]
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

        embed = embed_builder(title = f"{genius_song.title}",
                              title_url = genius_song_url,
                              description = genius_song_lyrics[:4096],
                              color = GENIUS_COLOR,
                              thumbnail = genius_song.header_image_thumbnail_url,
                              author = f"{genius_song.artist}",
                              author_icon = GENIUS_ICON,
                              footer = "Lyrics powered by Genius")

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "lyrics")

def setup(client):
    client.add_cog(lyrics(client))