import re

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.helpers import EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot



class Emoji(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["emoji"].alias,
        Commands().data["emoji"].description,
        name_localizations = {country_tag: Commands().data["emoji"].name for country_tag in nextcord.Locale},
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
    async def emoji(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        emoji: str = nextcord.SlashOption(
            Commands().data["emoji"].parameters["emoji"].name,
            Commands().data["emoji"].parameters["emoji"].description,
            required = True,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command reposts the original url of any custom emoji"""

        # re checks if it's a valid custom emoji format
        if not re.search(r"<(a:|:)[a-z0-9_]*:[0-9]*>", emoji, re.IGNORECASE):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a custom emoji."), ephemeral=True)
            return

        emote_animated = emoji.startswith("<a:")
        emoji_name, _, emoji_id = emoji.replace("<a:", "").replace("<:", "").replace(">", "").partition(":")

        partial_emoji_object = nextcord.PartialEmoji(name = emoji_name, animated = emote_animated, id = int(emoji_id))

        # check via the cdn if what we got was actually a valid emote
        if not requests.get(partial_emoji_object.url, timeout=10).status_code == 200:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a custom emoji."), ephemeral=True)
            return

        await interaction.response.send_message(f"`Link:` [{partial_emoji_object.name}]({partial_emoji_object.url})")



def setup(client: SomiBot) -> None:
    client.add_cog(Emoji(client))