import asyncio
import random

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Config
from lib.utilities import SomiBot



class Coinflip(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="coinflip", description="does a coinflip")
    async def coinflip(self, interaction: nextcord.Interaction) -> None:
        """This command does a coinflip with a small animation"""

        await interaction.response.defer(with_message=True)

        side1, side2 = random.sample([Config().HEADS_EMOTE, Config().TAILS_EMOTE], k=2)

        await interaction.followup.send(side1)

        # the first value in coin_animation's lists, is how long it is dispalyed and the 2nd which icon is shown
        for step in [[0.2, side2], [0.2, side1], [0.2, side2], [0.4, side1], [0.8, side2], [1, f"Result:\n{random.choice([side1, side2])}"]]:
            await asyncio.sleep(step[0])
            await interaction.edit_original_message(content = step[1])



def setup(client: SomiBot) -> None:
    client.add_cog(Coinflip(client))