import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Wolfram(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "wolfram", description = "find an answer to a query")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
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

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/wolfram",
            {"query": query}
        ))

        await interaction.response.defer(with_message = True)

        query_result = self.client.wolfram_client.query(query)

        try:
            await interaction.followup.send(f"Query: `{query}`\n```{next(query_result.results).text}```")
        except:
            await interaction.followup.send(embed=EmbedFunctions().error(f"Wolfram couldn't find a result for your query:\n`{query}`"))



def setup(client: SomiBot) -> None:
    client.add_cog(Wolfram(client))