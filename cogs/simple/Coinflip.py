###package#import###############################################################################

import asyncio
import nextcord
import random

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import HEADS, TAILS



class Coinflip(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###coinflip###########################################################
    
    @nextcord.slash_command(name = "coinflip", description = "does a coinflip")
    async def coinflip(self,
                       interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /coinflip")

        random_start = random.randint(0, 1)
        if random_start == 0:
            value1 = HEADS
            value2 = TAILS
        else:
            value1 = TAILS
            value2 = HEADS

        flip = random.randint(0, 1)
        if flip == 0:
            result = f"Result:\n{HEADS}"
        else:
            result = f"Result:\n{TAILS}"

        await interaction.response.send_message(value1)

        coin_animation = [[0.2, value2], [0.2, value1], [0.2, value2], [0.4, value1], [0.8, value2], [1, result]]

        for step in coin_animation:
            await asyncio.sleep(step[0])
            await interaction.edit_original_message(content = step[1])

        uses_update("command_uses", "coinflip")



def setup(client):
    client.add_cog(Coinflip(client))