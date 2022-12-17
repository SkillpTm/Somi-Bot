####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import wolframalpha

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Wolfram(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "wolfram", description = "find an answer to a query")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def wolfram(self,
                      interaction: nextcord.Interaction,
                      *,
                      query: str = nextcord.SlashOption(description="for what do you want an answer", required=True, min_length=2, max_length=200)):
        """This command uses the given query and sends it to the wolfram API, if a short answer can be found, it will be responded with"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /wolfram {query}")

        await interaction.response.defer(with_message = True)

        wolfram_client = wolframalpha.Client(self.client.Keychain.WOLFRAM_APP_ID)

        query_result = wolfram_client.query(query)

        try:
            await interaction.followup.send(f"Query: `{query}`\n```{next(query_result.results).text}```")
        except:
            await interaction.followup.send(embed=EmbedFunctions().error(f"Wolfram couldn't find a result for your query:\n`{query}`"))



def setup(client: SomiBot):
    client.add_cog(Wolfram(client))