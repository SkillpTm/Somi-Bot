####################################################################################################

import asyncio
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import random

####################################################################################################

from lib.modules import Checks
from lib.utilities import SomiBot



class Coinflip(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################
    
    @nextcord.slash_command(name = "coinflip", description = "does a coinflip")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def coinflip(self,
                       interaction: nextcord.Interaction):
        """This command does a coinflip with a small animation"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /coinflip")

        await interaction.response.defer(with_message=True)

        random_start = random.randint(0, 1)
        if random_start == 0:
            value1 = self.client.HEADS
            value2 = self.client.TAILS
        else:
            value1 = self.client.TAILS
            value2 = self.client.HEADS

        result = f"Result:\n{random.choice([self.client.HEADS, self.client.TAILS])}"

        await interaction.followup.send(value1)

        coin_animation = [[0.2, value2], [0.2, value1], [0.2, value2], [0.4, value1], [0.8, value2], [1, result]]

        for step in coin_animation:
            await asyncio.sleep(step[0])
            await interaction.edit_original_message(content = step[1])



def setup(client: SomiBot):
    client.add_cog(Coinflip(client))