###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import re

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import create_keyword
from utilities.maincommands import checks



class keyword_add(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import keyword

    ###keyword#add###########################################################
    
    @keyword.subcommand(name = "add", description = "add a keyword to your keyword list")
    async def keyword_add(self,
                          interaction: Interaction,
                          *,
                          keyword: str = SlashOption(description="Your new keyword", required=True, min_length=2, max_length=32)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /keyword add {keyword}")

        clean_keyword = str(keyword.lower().replace(" ", ""))

        is_lower_and_number = re.match("^[\da-z]+$", clean_keyword)

        if not is_lower_and_number:
            await interaction.response.send_message(f"You can only have letters and numbers in your keywords!", ephemeral=True)
            return

        added = create_keyword(interaction.user.id, clean_keyword)

        if not added:
            await interaction.response.send_message(f"You already have `{clean_keyword}` as a keyword.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your new keyword `{clean_keyword}` has been added to your keyword list.", ephemeral=True)

        uses_update("command_uses", "keyword add")

def setup(client):
    client.add_cog(keyword_add(client))