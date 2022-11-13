###package#import###############################################################################

import dotenv
import nextcord
import os
import spotipy

dotenv.load_dotenv()

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, embed_builder
from utilities.variables import SPOTIFY_ICON




spotifyOAuth = spotipy.SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                    redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                    scope="user-read-currently-playing")


token = spotifyOAuth.get_cached_token()
spotifyObject = spotipy.Spotify(auth=token['access_token'])

class Spotify(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###spotify###########################################################

    @nextcord.slash_command(name='sf', description='tells you what someone is listening to on Spotify', name_localizations = {country_tag:"spotify" for country_tag in nextcord.Locale})
    async def spotify(self,
                      interaction: nextcord.Interaction,
                      *,
                      member: nextcord.Member = nextcord.SlashOption(description="the user listening to Spotify", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        
        name = get_nick_else_name(member)

        print(f"{interaction.user}: /spotify {member}")

        token = spotifyOAuth.get_cached_token()
        spotifyObject = spotipy.Spotify(auth=token['access_token'])

        for activity in member.activities:
            if not isinstance(activity, nextcord.Spotify):
                continue

            track_spotipy = spotifyObject.track(f"spotify:track:{activity.track_id}")

            artists_with_urls = [f"[{artist['name']}]({artist['external_urls']['spotify']})" for artist in track_spotipy['artists']]

            album_url = track_spotipy['album']['external_urls']['spotify']
            album_name = track_spotipy['album']['name']

            track_url = track_spotipy['external_urls']['spotify']
            track_name = track_spotipy['name']

            cover_url = track_spotipy['album']['images'][0]['url']

            artists = ", ".join(map(str, artists_with_urls))

            embed = embed_builder(description = f"[{track_name}]({track_url})\non [{album_name}]({album_url})\nby {artists}",
                                  color = activity.color,
                                  thumbnail = cover_url,
                                  author = f"{name} is listening to:",
                                  author_icon = SPOTIFY_ICON,
                                  footer = "DEFAULT_KST_FOOTER")

            await interaction.response.send_message(embed=embed)

            uses_update("command_uses", "spotify")

            return

        await interaction.response.send_message(f"`{name}` isn't listening to anything on Spotify right now.", ephemeral=True)

        uses_update("command_uses", "spotify")



def setup(client):
    client.add_cog(Spotify(client))