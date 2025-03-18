import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import urllib.parse

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmNowPlaying(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "nowplaying", description = "shows what someone is listening to right now", name_localizations = {country_tag:"np" for country_tag in nextcord.Locale})
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
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if np_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
            return

        output, cover_image = self.get_and_format_output(np_response)

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image,
            author = f"{user.display_name} is listening to:",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)

    ####################################################################################################

    @staticmethod
    async def get_and_format_output(np_response: requests.Response) -> tuple[str, str]:
        """gets the data from the response and formats it to simply be output"""

        cover_image = ""
        output = ""

        # formats the last 2 songs for the output (also denotes if something is being listened to right now)
        for track in np_response.json()["recenttracks"]["track"]:
            track_url = track['url']
            artist_name_for_url = urllib.parse.quote_plus(track['artist']['#text'])
            album_name_for_url = urllib.parse.quote_plus(track['album']['#text'])

            track_name = Get.markdown_safe(track['name'])
            album_name = Get.markdown_safe(track['album']['#text'])
            artist_name = Get.markdown_safe(track['artist']['#text'])

            # check if this song is being listened to right now, or already was finished
            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
                output += f"**[{track_name}]({track_url})** on [{album_name}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}"
                if not cover_image:
                    cover_image = track['image'][3]['#text']

            else:
                output += f"`Now Playing:`\n**[{track_name}]({track_url})** on [{album_name}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/)\n\n`Previous:\n`"
                cover_image = track['image'][3]['#text']

        return output, cover_image



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmNowPlaying(client))