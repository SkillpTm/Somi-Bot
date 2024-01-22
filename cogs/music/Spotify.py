####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import spotipy

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Spotify(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name='sf', description='tells you what someone is listening to on Spotify', name_localizations = {country_tag:"spotify" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def spotify(self,
                      interaction: nextcord.Interaction,
                      *,
                      member: nextcord.Member = nextcord.SlashOption(description="the user listening to Spotify", required=False),
                      details: str = nextcord.SlashOption(description="do you want to get additional information on the song and artist", required=False, choices=["Yes", "No"])):
        """
        This command displays what song someone is playing currently, if they have their Spotify connected to their discord.
        To get data about a track, it uses the Spotipy API wrapper.
        """

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /spotify {member.id}")

        token = self.client.spotifyOAuth.get_cached_token()
        spotifyObject = spotipy.Spotify(auth=token['access_token'])

        member_activity: nextcord.Spotify = None

        for activity in member.activities:
            if isinstance(activity, nextcord.Spotify):
                member_activity = activity

        if not member_activity:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} isn't listening to anything on Spotify right now."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        track_spotipy = spotifyObject.track(f"spotify:track:{member_activity.track_id}")

        artists_with_urls = [f"[{artist['name']}]({artist['external_urls']['spotify']})" for artist in track_spotipy['artists']]

        album_url = track_spotipy['album']['external_urls']['spotify']
        album_name = track_spotipy['album']['name']

        track_url = track_spotipy['external_urls']['spotify']
        track_name = track_spotipy['name']

        cover_url = track_spotipy['album']['images'][0]['url']

        artists = ", ".join(map(str, artists_with_urls))

        fields = []

        if details == "Yes":
            track_duration_min = int(round(track_spotipy["duration_ms"] / 1000) / 60)
            track_duration_sec = round(track_spotipy["duration_ms"] / 1000) % 60
            track_duration = f"{track_duration_min}:{track_duration_sec}"

            if track_spotipy["explicit"]:
                track_explicit = "Yes"
            else:
                track_explicit = "No"

            artist_spotipy = spotifyObject.artist(f"spotify:artist:{track_spotipy['artists'][0]['id']}")


            fields = [
                [
                    "Track Duration:",
                    f"`{track_duration}`",
                    True
                ],

                [
                    "Track Explicit:",
                    track_explicit,
                    True
                ],

                [
                    "Track Popularity:",
                    f"`{int(track_spotipy['popularity'])}/100`",
                    True
                ],

                [
                    "Artist Followers:",
                    f"{'{:,}'.format(int(artist_spotipy['followers']['total']))}",
                    True
                ],

                [
                    "Artist Popularity:",
                    f"`{int(artist_spotipy['popularity'])}/100`",
                    True
                ],

                [
                    "Artist Genres:",
                    ", ".join(map(str, artist_spotipy['genres'])),
                    False
                ]
            ]




        embed = EmbedFunctions().builder(
            description = f"[{track_name}]({track_url})\non [{album_name}]({album_url})\nby {artists}",
            color = member_activity.color,
            thumbnail = cover_url,
            author = f"{member.display_name} is listening to:",
            author_icon = self.client.SPOTIFY_ICON,
            footer = "DEFAULT_KST_FOOTER",
            fields = fields
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Spotify(client))