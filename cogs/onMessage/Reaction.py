import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.managers import Config, Logger
from lib.modules import SomiBot



class Reactions(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def reaction(self, message: nextcord.Message) -> None:
        """makes the bot react to certain message contents"""               

        # react to pings
        if self.client.user.mentioned_in(message):
            await message.add_reaction(Config().REACTION_EMOTE)

            Logger().action_log(message, "reaction ping")

            await db.Telemetry.AMOUNT.increment("reacted @ping")


        # react to somionly
        if "somionly" in str(message.content.lower()):
            await message.add_reaction(Config().SOMI_ONLY_EMOTE)

            Logger().action_log(message, "reaction somionly")

            await db.Telemetry.AMOUNT.increment("reacted somionly")


        # react to a "f" in a message
        if re.search(rf"\b(f|{Config().SOMI_F_EMOTE.lower()})\b", message.content.lower()):
            await message.add_reaction(Config().SOMI_F_EMOTE)

            Logger().action_log(message, "reaction f")

            await db.Telemetry.AMOUNT.increment("reacted SomiF")

        # react to the somibestgrill emote
        if "somibestgrill" in str(message.content.lower()):
            await message.add_reaction(Config().SOMI_BEST_GRILL_EMOTE)

            Logger().action_log(message, "reaction bestgrill")

            await db.Telemetry.AMOUNT.increment("reacted SomiBestGrill")



def setup(client: SomiBot) -> None:
    client.add_cog(Reactions(client))