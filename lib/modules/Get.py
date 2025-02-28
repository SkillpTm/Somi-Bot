import datetime
import nextcord
import pytz
import re

from lib.utilities.SomiBot import SomiBot



class Get():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    @staticmethod
    def kst_timestamp(slash_kst_format: bool = False) -> str:
        """This function returns the current time as a humanreadable string"""

        now_korea = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

        if slash_kst_format:
            format = "Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"
        else:
            format = "%Y/%m/%d %H:%M:%S %Z"

        return now_korea.strftime(format)

    ####################################################################################################

    @staticmethod
    def seconds_from_time(time: str) -> int:
        """Converts a humanreadable time input into seconds:
            4h4s = 14404"""

        clean_time = time.replace(" ", "").lower()
        timeframes = re.findall(r"\d+[smhdwy]", clean_time)
        time_in_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}

        seconds = [int(timeframe[:-1]) * time_in_seconds[timeframe[-1]] for timeframe in timeframes]

        return sum(seconds)

    ####################################################################################################

    @staticmethod
    async def message_object_from_link(link: str,
                                       client: SomiBot) -> nextcord.Message | None :
        """Generates a message object from a discord message link input"""

        server_id, channel_id, message_id = re.search(r"/channels/(\d+)/(\d+)/(\d+)", link).groups()

        channel = await client.fetch_channel(channel_id)
        try:
            message: nextcord.Message = await channel.fetch_message(message_id)
        except:
            message = None

        return message

    ####################################################################################################

    @staticmethod
    def clean_input_command(commandname: str) -> str:
        """Makes an inputed commandname small, removes spaces and slahes"""

        commandname = commandname.replace(" ", "").replace("/", "")

        return commandname.lower()

    ####################################################################################################

    @staticmethod
    def autocomplete_dict_from_search_string(search_string: str, autocomplete_dict: dict) -> dict:
        """Takes a string and a dict and filters for matching results, between the two"""

        output = {}
        iteration = 0

        while iteration != 4:
            if len(output) == 25:
                    break

            for key, value in autocomplete_dict.items():
                if len(output) == 25:
                    break

                if iteration == 0 and str(value).lower().startswith(search_string.lower()):
                    output[str(key)] = str(value)
                    continue

                if iteration == 1 and search_string.lower() in str(value).lower():
                    output[str(key)] = str(value)
                    continue

                if iteration == 2 and str(key).lower().startswith(search_string.lower()):
                    output[str(key)] = str(value)
                    continue

                if iteration == 3 and search_string.lower() in str(key).lower():
                    output[str(key)] = str(value)
                    continue
            
            iteration += 1

        return output

    ####################################################################################################
    
    @staticmethod
    def markdown_safe(input_string: str) -> str:
        """Backslashes markdown relevant characters"""
        CHAR_AND_REPLACMENT = {
            "*": "＊",
            "_": "＿",
            "|": "｜",
            "#": "＃",
            "`": "｀",
            "[": "［",
            "]": "］",
            "(": "（",
            ")": "）",
            "<": "＜",
            ">": "＞",
            "-": "﹣",
        }

        for char, replacment in CHAR_AND_REPLACMENT.items():
            input_string = input_string.replace(char, replacment)

        return input_string

    ####################################################################################################

    @staticmethod
    def visible_users(client: SomiBot) -> set[int]:
        """Gets all unique user ids, of the users the client can see on all servers"""
        unique_users: set[int] = set()

        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    unique_users.add(member.id)

        return unique_users

    ####################################################################################################

    @staticmethod
    def rid_of_whitespace(string: str) -> str:
        """Removes leading whitesspace on all lines of a multi-line string"""

        string = "\n".join([line.strip() for line in string.split("\n")])

        return string
    
    ####################################################################################################

    @staticmethod
    def log_message(
        data_provider: nextcord.Interaction | nextcord.Message | nextcord.Member,
        action_name: str,
        action_args: dict[str, str] = {}
    ) -> str:
        """makes the log message for an interaction, message event or a member event"""

        # check if the data_provider is an Interaction or a Message
        if isinstance(data_provider, nextcord.Interaction) or isinstance(data_provider, nextcord.Member):
            aggregator_id = data_provider.user.id
        else:
            aggregator_id = data_provider.author.id

        ouput = ""

        ouput += f"{action_name} "
        ouput += f"~ User: {aggregator_id} "

        # check if the interaction was in a guild or dm
        if data_provider.guild:
            ouput += f"~ Guild: {data_provider.guild.id} "

            if data_provider.channel:
                ouput += f"~ Channel: {data_provider.channel.id} "
        else:
            ouput += "~ Guild: DM channel "

        ouput = "~ args: "
        for key, value in action_args.items():
            ouput = f"[{key}: {value}]"

        return ouput