import re

import nextcord
import nextcord.ext.application_checks as nextcord_AC



class Get():
    """Helper class holding methodes to get data"""

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
            output |= value

        return {key: value for index, (key, value) in enumerate(output.items()) if index < 25} # discord limits autocomplete suggestions to 25


    @staticmethod
    def clean_input_command(commandname: str) -> str:
        """Makes a commandname small, removes spaces and slahes"""

        return commandname.replace(" ", "").replace("/", "").lower()


    @staticmethod
    def interaction_by_owner() -> bool:
        """This function checks, if an interaction was made by the owner"""

        def predicate(interaction: nextcord.Interaction) -> bool:
            return interaction.user.id == interaction.client.owner_id

        return nextcord_AC.check(predicate)


    @staticmethod
    def markdown_safe(input_string: str) -> str:
        """Replaces markdown relevant characters with similar unicode chars to avoid issues, in places like embeds"""

        CHAR_AND_REPLACMENT = {
            "*": " ⃰ ",
            "_": "⎽",
            "|": "│",
            "#": "＃",
            "`": "ˋ",
            "[": "⦋",
            "]": "⦌",
            "(": "⦗",
            ")": "⦘",
            "<": "≤",
            ">": "≥",
            "-": "−",
        }

        for index, char in enumerate(input_string):
            if char in CHAR_AND_REPLACMENT:
                input_string[index] = CHAR_AND_REPLACMENT[char]

        return input_string


    @staticmethod
    def rid_of_whitespace(string: str) -> str:
        """Removes leading whitesspace on all lines of a multi-line string"""

        string = "\n".join([line.strip() for line in string.split("\n")])

        return string


    @staticmethod
    def seconds_from_time(time: str) -> int:
        """Converts a humanreadable time input into seconds: 4h4s = 14404"""

        time_in_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}
        timeframes = re.findall(r"[0-9]+[smhdwy]", time.replace(" ", "").lower())

        return sum([int(timeframe[:-1]) * time_in_seconds[timeframe[-1]] for timeframe in timeframes])