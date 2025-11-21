import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Keychain
from lib.modules import SomiBot



class Wolfram(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["wolfram"].name,
        Commands().data["wolfram"].description,
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def wolfram(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        query: str = nextcord.SlashOption(
            Commands().data["wolfram"].parameters["query"].name,
            Commands().data["wolfram"].parameters["query"].description,
            required = True,
            min_length = 2,
            max_length = 200
        )
    ) -> None:
        """This command uses the given query and sends it to the wolfram API, if a short answer can be found, it will be responded with"""

        await interaction.response.defer(with_message=True)

        try:
            await interaction.followup.send(f"Query: `{query}`\n```{next(Keychain().wolfram_client.query(query).results).text}```")
        except StopIteration:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"Wolfram couldn't find a result for your query:\n`{query}`"))



def setup(client: SomiBot) -> None:
    client.add_cog(Wolfram(client))