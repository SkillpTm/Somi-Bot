import urllib.parse

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Bang(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["bang"].alias,
        Commands().data["bang"].description,
        name_localizations = {country_tag: Commands().data["bang"].name for country_tag in nextcord.Locale},
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def bang(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        bang: str = nextcord.SlashOption(
            Commands().data["bang"].parameters["bang"].name,
            Commands().data["bang"].parameters["bang"].description,
            required = True,
            min_length = 1,
            max_length = 100
        ),
        query: str = nextcord.SlashOption(
            Commands().data["bang"].parameters["query"].name,
            Commands().data["bang"].parameters["query"].description,
            required = True,
            min_length = 1,
            max_length = 200,
        )
    ) -> None:
        """Allows users to use DuckDuckGo bangs to search things quickly"""

        bang = bang.strip("!").lower()

        if bang not in Config().BANG_LINKS.keys():
            await interaction.send(embed=EmbedFunctions.get_error_message(f"There is no bang with the name `{bang}`."), ephemeral=True)
            return

        await interaction.send(Config().BANG_LINKS[bang].replace(r"{{{s}}}", urllib.parse.quote_plus(query)))


    @bang.on_autocomplete("bang")
    async def bang_autocomplete_bang(self, interaction: nextcord.Interaction[SomiBot], bang: str) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(Get.autocomplete(bang.strip("!"), Config().BANG_TITLES))


def setup(client: SomiBot) -> None:
    client.add_cog(Bang(client))