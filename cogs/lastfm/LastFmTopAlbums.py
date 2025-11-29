import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain, Lists
from lib.modules import PageButtons, SomiBot



class LastFmTopAlbums(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(
        Commands().data["lf top-albums"].alias,
        Commands().data["lf top-albums"].description,
        name_localizations = {country_tag: Commands().data["lf top-albums"].name for country_tag in nextcord.Locale}
    )
    async def lastfm_top_albums(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf top-albums"].parameters["user"].name,
            Commands().data["lf top-albums"].parameters["user"].description,
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            Commands().data["lf top-albums"].parameters["timeframe"].name,
            Commands().data["lf top-albums"].parameters["timeframe"].description,
            required = False,
            choices = Lists().LASTFM_TIMEFRAMES
        )
    ) -> None:
        """This command shows someone's top albums"""

        user = user or interaction.user
        timeframe = timeframe or Lists().LASTFM_TIMEFRAMES["All Time"]

        if not (lastfm_username := str(await db.User.LASTFM.get(interaction.user.id) or "")):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        await self.lastfm_top_albums_rec(interaction, user, lastfm_username, timeframe, page_number = 1)


    async def lastfm_top_albums_rec(
        self,
        interaction: nextcord.Interaction[SomiBot],
        user: nextcord.User,
        lastfm_username: str,
        timeframe: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        top_albums_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if top_albums_response.status_code != 200:
            await interaction.edit_original_message(embed=EmbedFunctions.get_error_message("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        top_albums_data = top_albums_response.json()
        last_page = int(top_albums_data["topalbums"]["@attr"]["totalPages"])
        output = ""

        for album in top_albums_data["topalbums"]["album"]:
            album_url = album["url"]
            artist_url = album["artist"]["url"]

            album_name = Get.markdown_safe(album["name"])
            artist_name = Get.markdown_safe(album["artist"]["name"])
            output += f"`{album['@attr']['rank']}.` **[{album_name}]({album_url})** by [{artist_name}]({artist_url}) - *({album['playcount']} plays)*\n"

        footer = ""

        if (scrobbles_this_month := Get.lf_scrobbles_this_month(lastfm_username)) is not None:
            footer = f"{scrobbles_this_month} total Scrobbles, Past Month"

        embed = EmbedFunctions.builder(
            color = Config().LASTFM_COLOR,
            author = f"{user.display_name} Top Albums: {Lists().LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = Config().LASTFM_ICON,
            description = output,
            footer = footer,
            footer_icon = Config().HEADPHONES_ICON
        )

        view = PageButtons(page = page_number, last_page = last_page, interaction = interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_top_albums_rec(interaction, user, lastfm_username, timeframe, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTopAlbums(client))