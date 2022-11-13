###package#import###############################################################################

import dotenv
import nextcord
import os
import wolframalpha

dotenv.load_dotenv()

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class Wolfram(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###wolfram###########################################################

    @nextcord.slash_command(name = "wolfram", description = "find an answer to a query")
    async def wolfram(self,
                      interaction: nextcord.Interaction,
                      *,
                      query: str = nextcord.SlashOption(description="for what do you want an answer", required=True, min_length=1, max_length=200)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /wolfram {query}")

        await interaction.response.defer(with_message = True)

        client = wolframalpha.Client(os.getenv("WOLFRAM_APP_ID"))

        query_result = client.query(query)

        try:
            await interaction.followup.send(f"Query: `{query}`\n```{next(query_result.results).text}```")

        except:
            await interaction.followup.send(f"Wolfram couldn't find a result for your query:\n`{query}`")

        uses_update("command_uses", "wolfram")



def setup(client):
    client.add_cog(Wolfram(client))