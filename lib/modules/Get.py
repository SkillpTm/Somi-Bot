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
        """This function returns the current time in KST as a humanreadable string"""

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

        return sum([int(timeframe[:-1]) * time_in_seconds[timeframe[-1]] for timeframe in timeframes])

    ####################################################################################################

    @staticmethod
    async def message_object_from_link(link: str, client: SomiBot) -> nextcord.Message | None:
        """Generates a message object from a discord message link input"""

        _, channel_id, message_id = re.search(r"/channels/(\d+)/(\d+)/(\d+)", link).groups()

        channel = await client.fetch_channel(channel_id)
        try:
            message: nextcord.Message = await channel.fetch_message(message_id)
        except:
            message = None

        return message

    ####################################################################################################

    @staticmethod
    def clean_input_command(commandname: str) -> str:
        """Makes a commandname small, removes spaces and slahes"""

        return commandname.replace(" ", "").replace("/", "").lower()

    ####################################################################################################

    @staticmethod
    def autocomplete_dict_from_search_string(search_string: str, autocomplete_dict: dict) -> dict[str, str]:
        """Takes a string and a dict and filters for matching results, between the two. The results are sorted form most to least relevant."""

        search_string = search_string.lower()
        # dict[priority, dict[key, value]]
        priority_dict: dict[int, dict[str, str]] = {
            0: {},
            1: {},
            2: {},
            3: {}
        }

        # the key is what discord will display and the value what is actually behind it:
        # key: "50 Minutes" value: "50m"
        for key, value in autocomplete_dict.items():
            key, value = str(key), str(value)

            if len(priority_dict) == 25: # discord limits autocomplete suggestions to 25
                break

            # prority 0: search_string is the beginning of value
            if value.lower().startswith(search_string):
                priority_dict[0][key] = value
                continue

            # prority 1: search_string in the value
            if search_string in value.lower():
                priority_dict[1][key] = value
                continue

            # prority 2: search_string is the beginning of the key
            if key.lower().startswith(search_string):
                priority_dict[2][key] = value
                continue

            # prority 3: search_string in the key
            if search_string in key.lower():
                priority_dict[3][key] = value
                continue

        output: dict[str, str] = {}

        # merge the priority dicts, with higher priority results tkaing precedence over lower priority results
        for value in priority_dict.values():
            output = value | output

        return output

    ####################################################################################################
    
    @staticmethod
    def markdown_safe(input_string: str) -> str:
        """Replaces markdown relevant characters with similar unicode chars to avoid issues, in places like embeds"""

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
        """Gets a set of all unique user ids, the client can see"""
        
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
        data_provider: nextcord.Interaction | nextcord.Member | nextcord.User | nextcord.Message,
        action_name: str,
        action_args: dict[str, str] = {}
    ) -> str:
        """makes the log message for an interaction, member event, user event or message event"""

        # check if the data_provider is an Interaction, Member, User or Message top get the user's id
        if isinstance(data_provider, nextcord.Interaction) or isinstance(data_provider, nextcord.Member):
            aggregator_id = data_provider.user.id
        elif isinstance(data_provider, nextcord.User):
            aggregator_id = data_provider.id
        elif isinstance(data_provider, nextcord.Message):
            aggregator_id = data_provider.author.id

        ouput = ""

        ouput += f"{action_name} "
        ouput += f"~ User: {aggregator_id} "

        # check if the interaction was in a guild or dm
        if hasattr(data_provider, "guild"):
            ouput += f"~ Guild: {data_provider.guild.id} "

            if hasattr(data_provider, "channel"):
                ouput += f"~ Channel: {data_provider.channel.id} "
        elif hasattr(data_provider, "channel"):
            if data_provider.channel.type == nextcord.ChannelType.private:
                ouput += "~ Guild: DM channel "

        ouput = "~ args: "
        for key, value in action_args.items():
            ouput = f"[{key}: {value}]"

        return ouput