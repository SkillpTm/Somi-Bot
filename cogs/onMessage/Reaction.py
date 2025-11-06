import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import Get
from lib.utilities import SomiBot



class Reactions(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def reaction(self, message: nextcord.Message) -> None:
        """makes the bot react to certain message contents"""               

        # react to pings
        if self.client.user.mentioned_in(message):
            await message.add_reaction(self.client.config.REACTION_EMOTE)

            self.client.logger.action_log(Get.log_message(message, "reaction ping"))

            await (await DBHandler(self.client.database).telemetry()).increment("reacted @ping")


        # react to somionly
        if "somionly" in str(message.content.lower()):
            await message.add_reaction(self.client.config.SOMI_ONLY_EMOTE)

            self.client.logger.action_log(Get.log_message(message, "reaction somionly"))

            await (await DBHandler(self.client.database).telemetry()).increment("reacted somionly")


        # react to a "f" in a message
        if re.search(rf"\b(f|{self.client.config.SOMI_F_EMOTE.lower()})\b", message.content.lower()):
            await message.add_reaction(self.client.config.SOMI_F_EMOTE)

            self.client.logger.action_log(Get.log_message(message, "reaction f"))

            await (await DBHandler(self.client.database).telemetry()).increment("reacted SomiF")

        # react to the somibestgrill emote
        if "somibestgrill" in str(message.content.lower()):
            await message.add_reaction(self.client.config.SOMI_BEST_GRILL_EMOTE)

            self.client.logger.action_log(Get.log_message(message, "reaction bestgrill"))

            await (await DBHandler(self.client.database).telemetry()).increment("reacted SomiBestGrill")



def setup(client: SomiBot) -> None:
    client.add_cog(Reactions(client))