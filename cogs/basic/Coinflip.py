import asyncio
import nextcord
import nextcord.ext.commands as nextcord_C
import random

from lib.modules import Get
from lib.utilities import SomiBot



class Coinflip(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################
    
    @nextcord.slash_command(name="coinflip", description="does a coinflip")
    async def coinflip(self, interaction: nextcord.Interaction) -> None:
        """This command does a coinflip with a small animation"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/coinflip"))

        await interaction.response.defer(with_message=True)

        # make start icon random (for animation)
        if random.randint(0, 1):
            value1 = self.client.HEADS_EMOTE
            value2 = self.client.TAILS_EMOTE
        else:
            value1 = self.client.TAILS_EMOTE
            value2 = self.client.HEADS_EMOTE

        await interaction.followup.send(value1)

        # the first value in coin_animation's lists, is how long it is dispalyed and the 2nd which icon is shown
        result = f"Result:\n{random.choice([self.client.HEADS_EMOTE, self.client.TAILS_EMOTE])}"
        coin_animation = [[0.2, value2], [0.2, value1], [0.2, value2], [0.4, value1], [0.8, value2], [1, result]]

        for step in coin_animation:
            await asyncio.sleep(step[0])
            await interaction.edit_original_message(content = step[1])



def setup(client: SomiBot) -> None:
    client.add_cog(Coinflip(client))