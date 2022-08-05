###package#import###############################################################################

import os
import nextcord
from nextcord import Embed, Interaction, SlashOption, Spotify
from nextcord.ext import commands
import spotipy
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_get_title_name, get_spotify_track_data
from utilities.variables import SPOTIFY_ICON




spotifyOAuth = spotipy.SpotifyOAuth(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                    client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                                    redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'],
                                    scope="user-read-currently-playing")


token = spotifyOAuth.get_cached_token()
spotifyObject = spotipy.Spotify(auth=token['access_token'])

class spotify(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###spotify###########################################################

    @nextcord.slash_command(name='spotify', description='Tells you what someone is listening to on Spotify')
    async def spotify(self,
                      interaction: Interaction,
                      *,
                      member: nextcord.Member = SlashOption(description="The user listening to Spotify", required=False)):
        if not checks(interaction):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        
        title_name = embed_get_title_name(member)

        print(f"{interaction.user}: /spotify {member}")

        for activity in member.activities:
            if isinstance(activity, Spotify):
                track_spotipy = spotifyObject.track(f"spotify:track:{activity.track_id}")

                track_url, track_name, album_url, album_name, artist_urls, artists_list, cover_url = get_spotify_track_data(track_spotipy)

                artists_with_urls = []
                i = 0

                while i < len(artists_list):
                    artists_with_urls.append(f"[{artists_list[i]}]({artist_urls[i]})")
                    i += 1

                artists = ", ".join(map(str,artists_with_urls))
                
                embed = Embed(colour=activity.color,
                              description=f"[{track_name}]({track_url})\non [{album_name}]({album_url})\nby {artists}")
                embed_kst_footer(embed)
                embed.set_author(name= f"{title_name} is listening to:", icon_url=SPOTIFY_ICON)
                embed.set_thumbnail(url=cover_url)

                await interaction.send(embed=embed)

                uses_update("command_uses", "spotify")

                return

        embed_get_title_name(member)
        await interaction.response.send_message(f"`{title_name}` isn't listening to anything on Spotify right now.", ephemeral=True)

        uses_update("command_uses", "spotify")

    ###spotify#alias###########################################################

    @nextcord.slash_command(name='sf', description='Tells you what someone is listening to on Spotify')
    async def sf(self,
                 interaction: Interaction,
                 *,
                 member: nextcord.Member = SlashOption(description="The user listening to Spotify (alias of /spotify)", required=False)):
        if not checks(interaction):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        
        title_name = embed_get_title_name(member)

        print(f"{interaction.user}: /sf {member}")

        for activity in member.activities:
            if isinstance(activity, Spotify):
                track_spotipy = spotifyObject.track(f"spotify:track:{activity.track_id}")

                track_url, track_name, album_url, album_name, artist_urls, artists_list, cover_url = get_spotify_track_data(track_spotipy)

                artists_with_urls = []
                i = 0

                while i < len(artists_list):
                    artists_with_urls.append(f"[{artists_list[i]}]({artist_urls[i]})")
                    i += 1

                artists = ", ".join(map(str,artists_with_urls))
                
                embed = Embed(colour=activity.color,
                              description=f"[{track_name}]({track_url})\non [{album_name}]({album_url})\nby {artists}")
                embed_kst_footer(embed)
                embed.set_author(name= f"{title_name} is listening to:", icon_url=SPOTIFY_ICON)
                embed.set_thumbnail(url=cover_url)

                await interaction.send(embed=embed)

                uses_update("command_uses", "sf")

                return

        await interaction.response.send_message(f"`{title_name}` isn't listening to anything on Spotify right now.", ephemeral=True)

        uses_update("command_uses", "sf")

def setup(client):
    client.add_cog(spotify(client))