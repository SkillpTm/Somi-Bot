####################################################################################################

import lyricsgenius
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks, EmbedFunctions
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

        await interaction.response.defer(with_message=True)
        
        genius = lyricsgenius.Genius(self.client.Keychain.GENIUS_ACCESS_TOKEN)

        genius_song = genius.search_song(title=song, artist=artist)

        if not hasattr(genius_song, "lyrics"):
            await interaction.followup.send(embed=EmbedFunctions().error(f"Your search for:\nArtist: `{artist}`\nSong: `{song}`\n__failed__, please try again!"))
            return

        genius_song_lyrics = genius_song.lyrics[:-5] #Get rid of an error in the wrapper
        
        if genius_song_lyrics[len(genius_song_lyrics)-1].isdigit:
            genius_song_lyrics = genius_song_lyrics[:-1] #Get rid of another error in the wrapper

        embed = EmbedFunctions().builder(
            color = self.client.GENIUS_COLOR,
            thumbnail = genius_song.header_image_thumbnail_url,
            author = f"{genius_song.artist}",
            author_icon = self.client.GENIUS_ICON,
            title = f"{genius_song.title}",
            title_url = genius_song.url,
            description = genius_song_lyrics[:4096],
            footer = "Lyrics powered by Genius"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Lyrics(client))