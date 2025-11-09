import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Keychain
from lib.modules import PageButtons, SomiBot



class YouTube(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        Commands().data["youtube"].alias,
        Commands().data["youtube"].description,
        name_localizations = {country_tag: Commands().data["youtube"].name for country_tag in nextcord.Locale}
    )
    async def youtube(
        self,
        interaction: nextcord.Interaction,
        *,
        query: str = nextcord.SlashOption(
            Commands().data["youtube"].parameters["query"].name,
            Commands().data["youtube"].parameters["query"].description,
            required = True,
            min_length = 2,
            max_length = 200
        )
    ) -> None:
        """This command uses the given query and sends it to the YouTube Data API, then the user can flip thourgh the top 50 results"""

        await interaction.response.defer(with_message=True)

        search_result = Keychain().youtube.search().list(q=query, part="snippet", type="video", maxResults=50).execute()
        results = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in search_result["items"]]

        if not (results := [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in search_result["items"]]):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"YouTube couldn't find a video for your query:\n`{query}`"))
            return

        await interaction.followup.send(content=results[0])

        await self.youtube_rec(interaction=interaction, results=results, page_number=1)

    ####################################################################################################

    async def youtube_rec(
        self,
        interaction: nextcord.Interaction,
        results: list[str],
        page_number: int
    ) -> None:
        """This function recurses on button press and flips through the results gained earlier"""

        view = PageButtons(page = page_number, last_page = len(results), interaction = interaction)

        await interaction.edit_original_message(content=results[page_number-1], view=view)

        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.youtube_rec(interaction=interaction, results=results, page_number=view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(YouTube(client))