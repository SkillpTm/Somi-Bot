import logging

import nextcord

from lib.managers.Singleton import Singleton


class Logger(metaclass=Singleton):
    """Custom logger for bots actions, errors and wraps nextcoder's logger"""

    def __init__(self):
        action_handler = logging.FileHandler(filename="./debug/logs/action.log", encoding="utf-8", mode="a")
        action_handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s - %(levelname)s:\n%(message)s"))
        self.action_logger = logging.getLogger("SomiBot.Action")
        self.action_logger.setLevel(logging.DEBUG)
        self.action_logger.addHandler(action_handler)

        error_handler = logging.FileHandler(filename="./debug/logs/error.log", encoding="utf-8", mode="a")
        error_handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s - %(levelname)s:\n%(message)s"))
        self.error_logger = logging.getLogger("SomiBot.Error")
        self.error_logger.setLevel(logging.ERROR)
        self.error_logger.addHandler(error_handler)

        nextcord_handler = logging.FileHandler(filename="./debug/logs/nextcord.log", encoding="utf-8", mode="a")
        nextcord_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        self.nextcord_logger = logging.getLogger("nextcord")
        self.nextcord_logger.setLevel(logging.ERROR)
        self.nextcord_logger.addHandler(nextcord_handler)

    @staticmethod
    def get_log_message(
        data_provider: nextcord.Interaction | nextcord.Member | nextcord.User | nextcord.Message,
        action_name: str,
        action_inputs: list[dict] | list | dict | str = []
    ) -> str:
        """makes the log message for an interaction, member event, user event or message event"""

        aggregator_id = 0

        # check if the data_provider is an Interaction, Member, User or Message top get the user's id
        if isinstance(data_provider, nextcord.Interaction):
            aggregator_id = data_provider.user.id
        elif isinstance(data_provider, nextcord.Member):
            aggregator_id = data_provider.id
        elif isinstance(data_provider, nextcord.User):
            aggregator_id = data_provider.id
        elif isinstance(data_provider, nextcord.Message):
            aggregator_id = data_provider.author.id

        ouput = f"{action_name} ~ User: {aggregator_id} "

        # check if the interaction was in a guild or dm
        if hasattr(data_provider, "guild"):
            if data_provider.guild:
                ouput += f"~ Guild: {data_provider.guild.id} "

            if hasattr(data_provider, "channel"):
                if data_provider.channel:
                    ouput += f"~ Channel: {data_provider.channel.id} "
        elif hasattr(data_provider, "channel"):
            if data_provider.channel:
                if data_provider.channel.type == nextcord.ChannelType.private:
                    ouput += "~ Guild: DM channel "

        ouput += f"~ inputs: {action_inputs}"

        return ouput


    def action_log(
        self,
        data_provider: nextcord.Interaction | nextcord.Member | nextcord.User | nextcord.Message,
        action_name: str,
        action_inputs: list[dict] | list | dict | str = []
    )-> None:
        """Formats and logs a bot action"""
        self.action_logger.info(Logger.get_log_message(data_provider, action_name, action_inputs))


    def action_warning(self, action: str) -> None:
        """Formats and logs a bot warning"""
        self.action_logger.warning(action)


    def application_command_error(self, **kwargs) -> None:
        """Formats and logs a bot error"""
        error = ""

        for key, value in kwargs.items():
            error += f"{key}: {value}\n"

        self.error_logger.error(error)


    def bot_status(self, status: str) -> None:
        """Formats and logs a bot debug message"""
        self.action_logger.debug(status)