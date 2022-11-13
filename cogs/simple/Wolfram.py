###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import os
import wolframalpha
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class wolfram(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###wolfram###########################################################

    @nextcord.slash_command(name = "wolfram", description = "find an answer to a query")
    async def wolfram(self,
                      interaction: Interaction,
                      *,
                      query: str = SlashOption(description="for what do you want an answer", required=True, min_length=1, max_length=200)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /wolfram {query}")

        response = await interaction.response.send_message(f"Gathering answer...")

        client = wolframalpha.Client(os.getenv("WOLFRAM_APP_ID"))

        query_result = client.query(query)

        try:
            await response.edit(f"Query: `{query}`\n```{next(query_result.results).text}```")

        except:
            await response.edit(f"Wolfram couldn't find a result for your query:\n`{query}`")

        uses_update("command_uses", "wolfram")



def setup(client):
    client.add_cog(wolfram(client))