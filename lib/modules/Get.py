####################################################################################################

import datetime
import nextcord
import pytz
import re

####################################################################################################

from lib.utilities.SomiBot import SomiBot



class Get():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    @staticmethod
    def kst_timestamp(source: str = None) -> str:
        """This function returns the current time as a humanreadable string"""

        now_korea = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

        if source == "/kst":
            format = "Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"
        else:
            format = "%Y/%m/%d %H:%M:%S %Z"

        return now_korea.strftime(format)

    ####################################################################################################

    @staticmethod
    def seconds_from_time(time: str) -> int:
        """Converts a humanreadable time input into seconds:
            4h4s = 14400"""

        clean_time = time.replace(" ", "").lower()
        timeframes = re.findall(r"\d+[smhdwy]", clean_time)
        time_in_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}

        seconds = [int(timeframe[:-1]) * time_in_seconds[timeframe[-1]] for timeframe in timeframes]

        return sum(seconds)

    ####################################################################################################

    @staticmethod
    async def message_object_from_link(link: str,
                                       client: SomiBot) -> nextcord.Message:
        """Generates a message object from a discord message link input"""

        server_id, channel_id, message_id = re.search(r"/channels/(\d+)/(\d+)/(\d+)", link).groups()

        channel = await client.fetch_channel(channel_id)
        message: nextcord.Message = await channel.fetch_message(message_id)

        return message

    ####################################################################################################

    @staticmethod
    def clean_input_command(commandname: str) -> str:
        """Makes an inputed commandname small, removes spaces and slahes"""

        commandname = commandname.replace(" ", "").replace("/", "")

        return commandname.lower().replace("'", "‘")

    ####################################################################################################

    @staticmethod
    def autocomplete_dict_from_search_string(search_string: str, autocomplete_dict: dict) -> dict:
        """Takes a string and a list/dict and filters for matching results, between the two"""

        if search_string == "":
            full_keys_output = {}

            for key, value in autocomplete_dict.items():
                if len(full_keys_output) < 25:
                    full_keys_output.update({str(key): str(value)})

            return full_keys_output

        output = {}

        for key, value in autocomplete_dict.items():
            if str(value).lower().startswith(search_string.lower()) and len(output) < 25 and key not in output.keys():
                output.update({str(key): str(value)})

        if output == {}:
            for key, value in autocomplete_dict.items():
                if search_string.lower() in str(value).lower() and len(output) < 25 and key not in output.keys():
                    output.update({str(key): str(value)})

        if len(output) < 25:
            for key, value in autocomplete_dict.items():
                if str(key).lower().startswith(search_string.lower()) and len(output) < 25 and key not in output.keys():
                    output.update({str(key): str(value)})

            if output == {}:
                for key, value in autocomplete_dict.items():
                    if search_string.lower() in str(key).lower() and len(output) < 25 and key not in output.keys():
                        output.update({str(key): str(value)})

        return output

    ####################################################################################################
    
    @staticmethod
    def markdown_safe(input_string: str) -> str:
        CHAR_AND_REPLACMENT = {
            "*": "\*",
            "_": "\_",
            "[": "\[",
            "]": "\]",
            "#": "\#",
        }

        for char, replacment in CHAR_AND_REPLACMENT.items():
            input_string = input_string.replace(char, replacment)

        return input_string

    ####################################################################################################

    @staticmethod
    def visible_users(client: SomiBot) -> int:
        unique_users = set()

        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    unique_users.add(member.id)

        return len(unique_users)