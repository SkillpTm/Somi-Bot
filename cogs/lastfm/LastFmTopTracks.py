import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain, Lists
from lib.modules import PageButtons, SomiBot



class LastFmTopTracks(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(
        Commands().data["lf top-tracks"].alias,
        Commands().data["lf top-tracks"].description,
        name_localizations = {country_tag: Commands().data["lf top-tracks"].name for country_tag in nextcord.Locale}
    )
    async def lastfm_top_tracks(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf top-tracks"].parameters["user"].name,
            Commands().data["lf top-tracks"].parameters["user"].description,
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            Commands().data["lf top-tracks"].parameters["timeframe"].name,
            Commands().data["lf top-tracks"].parameters["timeframe"].description,
            required = False,
            choices = Lists().LASTFM_TIMEFRAMES
        )
    ) -> None:
        """This command shows someone's top tracks"""

        user = user or interaction.user
        timeframe = timeframe or "overall"

        if not (lastfm_username := await db.User.LASTFM.get(interaction.user.id)):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

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

        top_tarcks_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if not top_tarcks_response.status_code == 200:
            await interaction.edit_original_message(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        top_tracks_data = top_tarcks_response.json()
        last_page = int(top_tracks_data["toptracks"]["@attr"]["totalPages"])
        output = ""

        for track in top_tracks_data["toptracks"]["track"]:
            track_url = track["url"]
            artist_url = track["artist"]["url"]

            track_name = Get.markdown_safe(track["name"])
            artist_name = Get.markdown_safe(track["artist"]["name"])
            output += f"{track['@attr']['rank']}. **[{track_name}]({track_url})** by [{artist_name}]({artist_url}) - *({track['playcount']} plays)*\n"

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            author = f"{member.display_name} Top Tracks: {Lists().LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = Config().LASTFM_ICON,
            description = output
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