import logging



class Loggers():

    action_logger = logging.getLogger("SomiBot.Action")
    action_logger.setLevel(logging.DEBUG)

    action_handler = logging.FileHandler(filename="./storage/logs/action.log", encoding="utf-8", mode="a")
    action_handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s - %(levelname)s:\n%(message)s"))
    action_logger.addHandler(action_handler)


    error_logger = logging.getLogger("SomiBot.Error")
    error_logger.setLevel(logging.ERROR)

    error_handler = logging.FileHandler(filename="./storage/logs/error.log", encoding="utf-8", mode="a")
    error_handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s - %(levelname)s:\n%(message)s"))
    error_logger.addHandler(error_handler)


    nextcord_logger = logging.getLogger('nextcord')
    nextcord_logger.setLevel(logging.ERROR)

    nextcord_handler = logging.FileHandler(filename='./storage/logs/nextcord.log', encoding='utf-8', mode='a')
    nextcord_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    nextcord_logger.addHandler(nextcord_handler)

    ####################################################################################################

    def __init__(self) -> None:
        pass

    ####################################################################################################

    def bot_status(self,
                   status: str) -> None:
        self.action_logger.debug(status)

    ####################################################################################################

    def action_log(self,
                   action: str) -> None:
        self.action_logger.info(action)

    ####################################################################################################

    def action_warning(self,
                       action: str) -> None:
        self.action_logger.warning(action)

    ####################################################################################################

    def application_command_error(self, **kwargs) -> None:
        error = ""

        for key, value in kwargs.items():
            error += f"{key}: {value}\n"

        self.error_logger.error(error)