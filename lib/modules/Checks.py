import nextcord
import nextcord.ext.application_checks as nextcord_AC

from lib.utilities.SomiBot import SomiBot



class Checks():
    """This class supplies several static check methodes"""

    def __init__(self) -> None:
        pass

    ####################################################################################################

    @staticmethod
    def interaction_in_guild() -> bool:
        """This function checks, if an interaction occured in a guild"""

        def predicate(interaction: nextcord.Interaction) -> bool:
            return interaction.guild in interaction.client.guilds
        
        return nextcord_AC.check(predicate)

    ####################################################################################################

    @staticmethod
    def message_in_guild(client: SomiBot,message: nextcord.Message) -> bool:
        """This function checks, if a message was send in a guild"""

        return message.guild in client.guilds

    ####################################################################################################


    @staticmethod
    def interaction_not_by_bot() -> bool:
        """This function checks, if an interaction was created by a bot"""

        def predicate(interaction: nextcord.Interaction) -> bool:
            return not interaction.user.bot
        
        return nextcord_AC.check(predicate)
    
    ####################################################################################################

    @staticmethod
    def message_not_by_bot(message: nextcord.Message) -> bool:
        """This function checks, if a message was send by a bot"""

        return not message.author.bot
    
    ####################################################################################################

    @staticmethod
    def interaction_by_owner() -> bool:
        """This function checks, if an interaction was made by the owner"""

        def predicate(interaction: nextcord.Interaction) -> bool:
            return interaction.user.id == interaction.client.owner_id
        
        return nextcord_AC.check(predicate)