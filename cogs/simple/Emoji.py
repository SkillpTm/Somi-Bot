####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Emoji(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="emoji", description="make an emoji larger")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def emoji(self,
                    interaction: nextcord.Interaction,
                    *,
                    emoji: str = nextcord.SlashOption(description="your emoji", required=True, min_length=2, max_length=100)):
        """This command reposts the original url of any custom emoji"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /emoji {emoji}")

        if not emoji.startswith("<") and not emoji.endswith(">"):
            await interaction.response.send_message(embed=EmbedFunctions().error("Please select a custom emoji."), ephemeral=True)
            return

        if emoji.startswith("<a:"):
            emoji_name, sep, emoji_id = emoji[3:-1].partition(":")
            emote_animated = True
        else:
            emoji_name, sep, emoji_id = emoji[2:-1].partition(":")
            emote_animated = False

        partial_emoji_object = nextcord.PartialEmoji(name = emoji_name, id = emoji_id, animated = emote_animated)

        if not requests.get(partial_emoji_object.url).status_code == 200:
            await interaction.response.send_message(embed=EmbedFunctions().error("Please select a custom emoji."), ephemeral=True)
            return

        await interaction.response.send_message(partial_emoji_object.url)



def setup(client: SomiBot):
    client.add_cog(Emoji(client))