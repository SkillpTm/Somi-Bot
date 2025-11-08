import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Emoji(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "emote",
        description = "make an emoji larger",
        name_localizations = {country_tag:"emoji" for country_tag in nextcord.Locale}
    )
    async def emoji(
        self,
        interaction: nextcord.Interaction,
        *,
        emoji: str = nextcord.SlashOption(
            description = "your emoji",
            required = True,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command reposts the original url of any custom emoji"""

        # check if basic syntax for an emoji is met
        if not emoji.startswith("<") and not emoji.endswith(">"):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a custom emoji."), ephemeral=True)
            return

        # check if the emoji is animated or not
        if emoji.startswith("<a:"):
            emoji_name, _, emoji_id = emoji[3:-1].partition(":")
            emote_animated = True
        else:
            emoji_name, _, emoji_id = emoji[2:-1].partition(":")
            emote_animated = False

        partial_emoji_object = nextcord.PartialEmoji(name = emoji_name, id = emoji_id, animated = emote_animated)

        # check via the cdn if what we got was actually a valid emote
        if not requests.get(partial_emoji_object.url, timeout=10).status_code == 200:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a custom emoji."), ephemeral=True)
            return

        await interaction.response.send_message(f"`Link:` [{partial_emoji_object.name}]({partial_emoji_object.url})")



def setup(client: SomiBot) -> None:
    client.add_cog(Emoji(client))