###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class emoji(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###emoji###########################################################

    @nextcord.slash_command(name="emoji", description="make an emoji larger")
    async def emoji(self,
                    interaction: Interaction,
                    *,
                    emoji: str = SlashOption(description="your emoji", required=True, min_length=1, max_length=100)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /emoji {emoji}")

        head, sep, emoji_id = emoji[3:-1].partition(":")
        emoji_url = "https://cdn.discordapp.com/emojis/None"

        if emoji.startswith("<a:"):
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
        elif emoji.startswith("<:"):
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.webp"

        if not requests.get(emoji_url).status_code == 200:
            await interaction.response.send_message("Please select an emoji.", ephemeral=True)
            return

        await interaction.response.send_message(emoji_url)

        uses_update("command_uses", "emoji")

def setup(client):
    client.add_cog(emoji(client))