####################################################################################################

import nextcord
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.utilities.SomiBot import SomiBot



class Checks():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    @staticmethod
    def interaction_in_guild() -> bool:
        """This function checks, if an interaction occured in a guild and wasn't initiate by a bot"""

        def predicate(interaction: nextcord.Interaction) -> bool:
            return interaction.guild in interaction.client.guilds and interaction.user.bot == False
        return nextcord_AC.check(predicate)

    ####################################################################################################

    @staticmethod
    def message_in_guild(client: SomiBot,
                         message: nextcord.Message) -> bool:
        """This function checks, if a message was send in a guild and wasn't send by a bot"""

        return message.guild in client.guilds and message.author.bot == False

    