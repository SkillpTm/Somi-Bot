####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import spotipy

####################################################################################################

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Spotify(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name='sf',
        description='tells you what someone is listening to on Spotify',
        name_localizations = {country_tag:"spotify" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def spotify(
        self,
        interaction: nextcord.Interaction,
        *,
        member: nextcord.Member = nextcord.SlashOption(
            description="the user listening to Spotify",
            required=False
        ),
        details: str = nextcord.SlashOption(
            description="do you want to get additional information on the song and artist",
            required=False,
            choices=["Yes", "No"]
        )
    ) -> None:
        """
        This command displays what song someone is playing currently, if they have their Spotify connected to their discord.
        To get data about a track, it uses the Spotipy API wrapper.
        """

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/spotify",
            {"member": str(member.id), "details": details}
        ))

        member_activity: nextcord.Spotify = None

        # check the members activities for Spotify
        for activity in member.activities:
            if isinstance(activity, nextcord.Spotify):
                member_activity = activity
                break

        if not member_activity:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} isn't listening to anything on Spotify right now."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        output_data = self.get_output_data(member_activity, details)

        embed = EmbedFunctions().builder(
            description = f"[{output_data['track_name']}]({output_data['track_url']})\non [{output_data['album_name']}]({output_data['album_url']})\nby {output_data['artists']}",
            color = member_activity.color,
            thumbnail = output_data["cover_url"],
            author = f"{member.display_name} is listening to:",
            author_icon = self.client.SPOTIFY_ICON,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Track Duration:",
                    output_data["track_duration"],
                    True
                ],

                [
                    "Track Explicit:",
                    output_data["track_explicit"],
                    True
                ],

                [
                    "Track Popularity:",
                    output_data["track_popularity"],
                    True
                ],

                [
                    "Artist Followers:",
                    output_data["artist_followers"],
                    True
                ],

                [
                    "Artist Popularity:",
                    output_data["artist_popularity"],
                    True
                ],

                [
                    "Artist Genres:",
                    output_data["artist_genres"],
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)

    ####################################################################################################

    async def get_output_data(
        self,
        member_activity: nextcord.Spotify,
        details: str
    ) -> dict[str, str]:
        """uses the Spotify API to get the output data (potentially with details, if specified)"""

        spotify_object = spotipy.Spotify(auth=self.client.spotifyOAuth.get_cached_token()['access_token'])
        track_data = spotify_object.track(f"spotify:track:{member_activity.track_id}")
        artist_data = spotify_object.artist(f"spotify:artist:{track_data['artists'][0]['id']}")
        output_data: dict[str, str] = {}

        # the artists are seperated by commas and have a markdown link to their SF page on them: [name](link), [name2](link2)...
        output_data["artists"] = ", ".join([f"[{artist['name']}]({artist['external_urls']['spotify']})" for artist in track_data['artists']])
        output_data["album_name"] = track_data['album']['name']
        output_data["album_url"] = track_data['album']['external_urls']['spotify']
        output_data["cover_url"] = track_data['album']['images'][0]['url']
        output_data["track_name"] = track_data['name']
        output_data["track_url"] = track_data['external_urls']['spotify']

        if details == "Yes":
            output_data["artist_genres"] = ", ".join(artist_data['genres'])
            output_data["artist_followers"] = "{:,}".format(int(artist_data['followers']['total']))
            output_data["artist_popularity"] = f"`{int(artist_data['popularity'])}/100`"
            output_data["track_duration"] = f"`{int(round(track_data['duration_ms'] / 1000) / 60)}:{round(track_data['duration_ms'] / 1000) % 60}`"
            output_data["track_popularity"] = f"`{int(track_data['popularity'])}/100`"
            if track_data["explicit"]:
                output_data["track_explicit"] = "Yes"
            else:
                output_data["track_explicit"] = "No"
        else:
            # if the value of a field is an empty string it gets hidden, meaning if details is set to "No" no field will be displayed
            output_data["artist_genres"] = ""
            output_data["artist_followers"] = ""
            output_data["artist_popularity"] = ""
            output_data["track_duration"] = ""
            output_data["track_popularity"] = ""
            output_data["track_explicit"] = ""

        return output_data



def setup(client: SomiBot) -> None:
    client.add_cog(Spotify(client))