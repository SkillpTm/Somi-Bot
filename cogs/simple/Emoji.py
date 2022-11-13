###package#import###############################################################################

import nextcord
import requests

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class Emoji(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###emoji###########################################################

    @nextcord.slash_command(name="emoji", description="make an emoji larger")
    async def emoji(self,
                    interaction: nextcord.Interaction,
                    *,
                    emoji: str = nextcord.SlashOption(description="your emoji", required=True, min_length=1, max_length=100)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /emoji {emoji}")

        if not emoji.startswith("<") and not emoji.endswith(">"):
            await interaction.response.send_message("Please select an emoji.", ephemeral=True)
            return

        if emoji.startswith("<a:"):
            emoji_name, sep, emoji_id = emoji[3:-1].partition(":")
            emote_animated = True
        else:
            emoji_name, sep, emoji_id = emoji[2:-1].partition(":")
            emote_animated = False

        partial_emoji_object = nextcord.PartialEmoji(name = emoji_name, id = emoji_id, animated = emote_animated)

        if not requests.get(partial_emoji_object.url).status_code == 200:
            await interaction.response.send_message("Please select an emoji.", ephemeral=True)
            return

        await interaction.response.send_message(partial_emoji_object.url)

        uses_update("command_uses", "emoji")



def setup(client):
    client.add_cog(Emoji(client))