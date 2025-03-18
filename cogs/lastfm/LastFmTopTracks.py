import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, PageButtons, SomiBot



class LastFmTopTracks(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(name = "tt", description = "shows your top tracks on LastFm", name_localizations = {country_tag:"toptracks" for country_tag in nextcord.Locale})
    async def lastfm_top_tracks(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want the top tracks of",
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            description = "the timeframe you want the top tracks for",
            required = False,
            choices = Lists.LASTFM_TIMEFRAMES
        )
    ) -> None:
        """This command shows someone's top tracks"""

        if not user:
            user = interaction.user

        if not timeframe:
            timeframe = "overall"

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf toptracks",
            {"user": str(user.id), "timeframe": timeframe}
        ))

        lastfm_username = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_get()

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        await self.lastfm_top_tracks_rec(interaction, user, lastfm_username, timeframe, page_number = 1)

    ####################################################################################################

    async def lastfm_top_tracks_rec(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member,
        lastfm_username: str,
        timeframe: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        top_tarcks_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if not top_tarcks_response.status_code == 200:
            await interaction.edit_original_message(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        top_tracks_data = top_tarcks_response.json()
        last_page = int(top_tracks_data["toptracks"]["@attr"]["totalPages"])
        output = ""

        for track in top_tracks_data["toptracks"]["track"]:
            track_url = track['url']
            artist_url = track['artist']['url']

            track_name = Get.markdown_safe(track['name'])
            artist_name = Get.markdown_safe(track['artist']['name'])
            output += f"{track['@attr']['rank']}. **[{track_name}]({track_url})** by [{artist_name}]({artist_url}) - *({track['playcount']} plays)*\n"

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            author = f"{member.display_name} Top Tracks: {Lists.LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        view = PageButtons(page = page_number, last_page = last_page, interaction = interaction)

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_top_tracks_rec(interaction, member, lastfm_username, timeframe, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTopTracks(client))