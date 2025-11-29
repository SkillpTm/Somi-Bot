import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Keychain
from lib.modules import SomiBot



class Spotify(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["spotify"].alias,
        Commands().data["spotify"].description,
        name_localizations = {country_tag: Commands().data["spotify"].name for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def spotify(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["spotify"].parameters["member"].name,
            Commands().data["spotify"].parameters["member"].description,
            required = False
        ),
        details: typing.Literal["Yes", ""] = nextcord.SlashOption(
            Commands().data["spotify"].parameters["details"].name,
            Commands().data["spotify"].parameters["details"].description,
            required = False,
            choices = ["Yes"],
            default = ""
        )
    ) -> None:
        """
        This command displays what song someone is playing currently, if they have their Spotify connected to their discord.
        To get data about a track, it uses the Spotipy API wrapper.
        """

        member = member or interaction.guild.get_member(interaction.user.id)
        member_activity: nextcord.Spotify | None = None

        # check the members activities for Spotify
        for activity in member.activities:
            if isinstance(activity, nextcord.Spotify):
                member_activity = activity
                break

        if not member_activity:
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{member.mention} isn't listening to anything on Spotify right now."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        output_data = await self.get_output_data(member_activity, details)

        embed = EmbedFunctions.builder(
            description = f"on `{output_data['album_name']}`",
            color = member_activity.color,
            image = output_data["cover_url"],
            author = f"{output_data['track_name']} - {output_data['artists']}",
            author_url = output_data['track_url'],
            author_icon = Config().SPOTIFY_ICON,
            footer = "Now Playing",
            footer_icon = Config().HEADPHONES_ICON,
            fields = [
                EmbedField(
                    "Track Duration:",
                    output_data["track_duration"],
                    True
                ),
                EmbedField(
                    "Track Explicit:",
                    output_data["track_explicit"],
                    True
                ),
                EmbedField(
                    "Track Popularity:",
                    output_data["track_popularity"],
                    True
                ),
                EmbedField(
                    "Artist Followers:",
                    output_data["artist_followers"],
                    True
                ),
                EmbedField(
                    "Artist Popularity:",
                    output_data["artist_popularity"],
                    True
                ),
                EmbedField(
                    "Artist Genres:",
                    output_data["artist_genres"],
                    False
                )
            ]
        )

        await interaction.send(embed=embed)


    async def get_output_data(
        self,
        member_activity: nextcord.Spotify,
        details: typing.Literal["Yes", ""]
    ) -> dict[str, str]:
        """uses the Spotify API to get the output data (potentially with details, if specified)"""

        track_data: dict[str, typing.Any] = Keychain().spotipy.track(f"spotify:track:{member_activity.track_id}") # type: ignore
        artist_data: dict[str, typing.Any] = Keychain().spotipy.artist(f"spotify:artist:{track_data['artists'][0]['id']}") # type: ignore
        output_data: dict[str, str] = {}

        # the artists are seperated by commas and have a markdown link to their SF page on them: [name](link), [name2](link2)...
        output_data["artists"] = ", ".join([artist["name"] for artist in track_data["artists"]])
        output_data["album_name"] = track_data["album"]["name"]
        output_data["album_url"] = track_data["album"]["external_urls"]["spotify"]
        output_data["cover_url"] = track_data["album"]["images"][0]["url"]
        output_data["track_name"] = track_data["name"]
        output_data["track_url"] = track_data["external_urls"]["spotify"]

        if details == "Yes":
            output_data["artist_genres"] = ", ".join(artist_data["genres"])
            output_data["artist_followers"] = f"{int(artist_data["followers"]["total"]):,}"
            output_data["artist_popularity"] = f"`{int(artist_data['popularity'])}/100`"
            output_data["track_duration"] = f"`{int(round(track_data['duration_ms'] / 1000) / 60)}:{round(track_data['duration_ms'] / 1000) % 60}`"
            output_data["track_popularity"] = f"`{int(track_data['popularity'])}/100`"
            output_data["track_explicit"] = "Yes" if track_data["explicit"] else "No"
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