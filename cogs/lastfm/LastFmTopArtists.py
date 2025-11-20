import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain, Lists
from lib.modules import PageButtons, SomiBot



class LastFmTopArtists(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(
        Commands().data["lf top-artists"].alias,
        Commands().data["lf top-artists"].description,
        name_localizations = {country_tag: Commands().data["lf top-artists"].name for country_tag in nextcord.Locale}
    )
    async def lastfm_top_artists(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf top-artists"].parameters["user"].name,
            Commands().data["lf top-artists"].parameters["user"].description,
            required = False
        ),
        timeframe: str = nextcord.SlashOption(
            Commands().data["lf top-artists"].parameters["timeframe"].name,
            Commands().data["lf top-artists"].parameters["timeframe"].description,
            required = False,
            choices = Lists().LASTFM_TIMEFRAMES
        )
    ) -> None:
        """This command shows someone's top artists"""

        user = user or interaction.user
        timeframe = timeframe or "overall"

        if not (lastfm_username := str(await db.User.LASTFM.get(interaction.user.id) or "")):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        # send a dummy respone to be updated in the recursive function
        await interaction.response.send_message(embed=EmbedFunctions().builder(title=" "))

        await self.lastfm_top_artists_rec(interaction, user, lastfm_username, timeframe, page_number = 1)


    async def lastfm_top_artists_rec(
        self,
        interaction: nextcord.Interaction[SomiBot],
        user: nextcord.User,
        lastfm_username: str,
        timeframe: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        top_artists_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if top_artists_response.status_code != 200:
            await interaction.edit_original_message(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        top_artists_data = top_artists_response.json()
        last_page = int(top_artists_data["topartists"]["@attr"]["totalPages"])
        output = ""

        for artist in top_artists_data["topartists"]["artist"]:
            artist_url = artist["url"]

            artist_name = Get.markdown_safe(artist["name"])
            output += f"{artist['@attr']['rank']}. **[{artist_name}]({artist_url})** - *({artist['playcount']} plays)*\n"

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            author = f"{user.display_name} Top Artists: {Lists().LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = Config().LASTFM_ICON,
            description = output
        )

        view = PageButtons(page=page_number, last_page=last_page, interaction=interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_top_artists_rec(interaction, user, lastfm_username, timeframe, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTopArtists(client))