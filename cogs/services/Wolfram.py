import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Wolfram(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="wolfram", description="find an answer to a query")
    async def wolfram(
        self,
        interaction: nextcord.Interaction,
        *,
        query: str = nextcord.SlashOption(
            description = "for what do you want an answer",
            required = True,
            min_length = 2,
            max_length = 200
        )
    ) -> None:
        """This command uses the given query and sends it to the wolfram API, if a short answer can be found, it will be responded with"""

        await interaction.response.defer(with_message=True)

        try:
            await interaction.followup.send(f"Query: `{query}`\n```{next(self.client.wolfram_client.query(query).results).text}```")
        except StopIteration:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"Wolfram couldn't find a result for your query:\n`{query}`"))



def setup(client: SomiBot) -> None:
    client.add_cog(Wolfram(client))