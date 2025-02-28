import nextcord
import nextcord.ext.commands as nextcord_C
import re

from lib.db_modules import CommandUsesDB
from lib.modules import Get
from lib.utilities import SomiBot



class Reactions(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def reaction(self, message: nextcord.Message) -> None:
        """makes the bot react to certain message contents"""               

        # react to ings
        if self.client.user.mentioned_in(message):
            await message.add_reaction(self.client.REACTION_EMOTE)

            self.client.Loggers.action_log(Get().log_message(message, "reaction ping"))

            CommandUsesDB("log_activations").update("reacted @ping")


        # react to somionly
        if "somionly" in str(message.content.lower()):
            await message.add_reaction(self.client.SOMI_ONLY_EMOTE)

            self.client.Loggers.action_log(Get().log_message(message, "reaction somionly"))

            CommandUsesDB("log_activations").update("reacted somionly")


        # react to a "f" in a message
        if any(f_string in f" {message.content.lower()} " for f_string in [" f ", "\nf ", " f\n", self.SOMI_F_EMOTE.lower()]):
            await message.add_reaction(self.client.SOMI_F_EMOTE)

            self.client.Loggers.action_log(Get().log_message(message, "reaction f"))

            CommandUsesDB("log_activations").update("reacted SomiF")

        # react to the somibestgrill emote
        if "somibestgrill" in str(message.content.lower()):
            await message.add_reaction(self.client.SOMI_BEST_GRILL_EMOTE)

            self.client.Loggers.action_log(Get().log_message(message, "reaction bestgrill"))

            CommandUsesDB("log_activations").update("reacted SomiBestGrill")


def setup(client: SomiBot) -> None:
    client.add_cog(Reactions(client))