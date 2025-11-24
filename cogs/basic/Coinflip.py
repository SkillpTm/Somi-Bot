import asyncio
import random

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Commands, Config
from lib.modules import SomiBot



class Coinflip(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["coinflip"].name,
        Commands().data["coinflip"].description,
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
    async def coinflip(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command does a coinflip with a small animation"""

        await interaction.response.defer(with_message=True)

        side1, side2 = random.sample([Config().HEADS_EMOTE, Config().TAILS_EMOTE], k=2)

        await interaction.send(side1)

        animation: list[tuple[float, str]] = [(0.2, side2), (0.2, side1), (0.2, side2), (0.4, side1), (0.8, side2), (1.0, f"Result:\n{random.choice([side1, side2])}")]

        # the first value in coin_animation's lists, is how long it is dispalyed and the 2nd which icon is shown
        for step in animation:
            await asyncio.sleep(step[0])
            await interaction.edit_original_message(content = step[1])



def setup(client: SomiBot) -> None:
    client.add_cog(Coinflip(client))