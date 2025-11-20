import datetime

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain
from lib.modules import SomiBot



class LastFmNowPlaying(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(
        Commands().data["lf now-playing"].alias,
        Commands().data["lf now-playing"].description,
        name_localizations = {country_tag: Commands().data["lf now-playing"].name for country_tag in nextcord.Locale}
    )
    async def lastfm_now_playing(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf now-playing"].parameters["user"].name,
            Commands().data["lf now-playing"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command displays what someone last listend to (and what they're listening to right now)"""

        user = user or interaction.user

        if not (lastfm_username := await db.User.LASTFM.get(interaction.user.id)):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if np_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
            return
        
        album_name, artist_name, cover_url, track_name, track_url, timestamp = "", "", "", "", "", None

        # lastfm will respond with 2 tracks, if the user is listening to a song right now, otherwise just one
        for track in np_response.json()["recenttracks"]["track"]:
            album_name = Get.markdown_safe(track["album"]["#text"])
            artist_name = Get.markdown_safe(track["artist"]["#text"])
            cover_url = track["image"][3]["#text"]
            track_name = Get.markdown_safe(track["name"])
            track_url = track["url"]

            # check if this song is being listened to right now, or already was finished
            if "@attr" in track.keys() and "nowplaying" in track["@attr"].keys():
                timestamp = None
            else:
                timestamp = datetime.datetime.fromtimestamp(float(track['date']['uts']))

            break

        if not timestamp:
            footer = "Now Playing"
            footer_icon = Config().HEADPHONES_ICON
        else:
            footer = "Listened:"
            footer_icon = ""

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            image = cover_url,
            author = f"{track_name} - {artist_name}",
            author_url = track_url,
            author_icon = Config().LASTFM_ICON,
            description = f"on `{album_name}`",
            footer = footer,
            footer_icon = footer_icon,
            footer_timestamp = timestamp
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmNowPlaying(client))