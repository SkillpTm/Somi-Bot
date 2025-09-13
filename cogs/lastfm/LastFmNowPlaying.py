import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import datetime

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmNowPlaying(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(
        name = "np",
        description = "shows what someone is listening to right now",
        name_localizations = {country_tag:"now-playing" for country_tag in nextcord.Locale}
    )
    async def lastfm_now_playing(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want to be shown, what they're listening to",
            required = False
        )
    ) -> None:
        """This command displays what someone last listend to (and what they're listening to right now)"""

        if not user:
            user = interaction.user

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf np",
            {"user": str(user.id)}
        ))

        lastfm_username = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_get()

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if np_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
            return

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
            footer_icon = self.client.HEADPHONES_ICON
        else:
            footer = "Listened:"
            footer_icon = ""

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            image = cover_url,
            author = f"{track_name} - {artist_name}",
            author_url = track_url,
            author_icon = self.client.LASTFM_ICON,
            description = f"on `{album_name}`",
            footer = footer,
            footer_icon = footer_icon,
            footer_timestamp = timestamp
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmNowPlaying(client))