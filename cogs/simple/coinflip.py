###package#import###############################################################################

import asyncio
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import random

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import HEADS, TAILS



class coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###coinflip###########################################################
    
    @nextcord.slash_command(name = "coinflip", description = "does a coinflip")
    async def coinflip(self,
                       interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /coinflip")

        flip = random.randint(0, 1)
        random_start = random.randint(0, 1)
        if random_start == 0:
            value1= HEADS
            value2= TAILS
        else:
            value1= TAILS
            value2= HEADS

        await interaction.response.send_message(value1)

        channel_id = self.client.get_channel(interaction.channel.id)
        bot_reply = (await channel_id.history(limit=1).flatten())[0]

        await asyncio.sleep(0.2)
        await bot_reply.edit(value2)
        await asyncio.sleep(0.2)
        await bot_reply.edit(value1)
        await asyncio.sleep(0.2)
        await bot_reply.edit(value2)
        await asyncio.sleep(0.4)
        await bot_reply.edit(value1)
        await asyncio.sleep(0.8)
        await bot_reply.edit(value2)
        await asyncio.sleep(1)

        if flip == 0:
            await bot_reply.edit(f"Result:\n{HEADS}")

        if flip == 1:
            await bot_reply.edit(f"Result:\n{TAILS}")

        uses_update("command_uses", "coinflip")

def setup(client):
    client.add_cog(coinflip(client))