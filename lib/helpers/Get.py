import re
import time

from lib.managers import Keychain

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests



class Get():
    """Helper class holding methodes to get data"""

    @staticmethod
    def autocomplete(neddle: str, haystack: dict[str, str] | list[str] | set[str]) -> dict[str, str]:
        """Takes a string and a dict and filters for matching results, between the two. The results are sorted form most to least relevant."""

        CHAR_LIMIT = 100
        AMOUNT_LIMIT = 25

        if not isinstance(haystack, dict):
            haystack = {item: item for item in haystack}

        neddle = neddle.lower()
        # dict[priority, dict[key, value]]
        priority_dict: dict[int, dict[str, str]] = {
            0: {},
            1: {},
            2: {},
            3: {}
        }

        # the key is what discord will display and the value what is actually behind it:
        # key: "50 Minutes" value: "50m"
        for key, value in haystack.items():
            key, value = str(key), str(value)

            # neddle is the beginning of value
            if value.lower().startswith(neddle):
                priority = 0
            # neddle in the value
            elif neddle in value.lower():
                priority = 1
            # neddle is the beginning of the key
            elif key.lower().startswith(neddle):
                priority = 2
            # neddle in the key
            elif neddle in key.lower():
                priority = 3
            # neddle is not found
            else:
                priority = None

            if priority is not None:
                key = f"{key[:CHAR_LIMIT-3]}..." if len(key) > CHAR_LIMIT else key
                priority_dict[priority][key] = value[:CHAR_LIMIT]

        output: dict[str, str] = {}

        # merge the priority dicts, with higher priority results taking precedence over lower priority results
        for value in priority_dict.values():
            output |= value

        return {key: value for index, (key, value) in enumerate(output.items()) if index < AMOUNT_LIMIT}


    @staticmethod
    def clean_input_command(commandname: str) -> str:
        """Makes a commandname small, removes spaces and slahes"""

        return commandname.replace(" ", "").replace("/", "").lower()


    @staticmethod
    def interaction_by_owner(): # type: ignore -> there doesn't seem to be a good type to hint this with?
        """This function checks, if an interaction was made by the owner"""

        def predicate(interaction: nextcord.Interaction[nextcord_C.Bot]) -> bool:
            return interaction.user.id == interaction.client.owner_id

        return nextcord_AC.check(predicate)


    @staticmethod
    def lf_scrobbles_this_month(lastfm_username: str) -> int | None:
        """Gets the amount of scrobbles a user has this month from LastFm, returns None on failure"""

        now_last_month = int(time.time()) - 60 * 60* 24 * 30

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&page=1&from={now_last_month}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if np_response.status_code != 200:
            return None

        return int(np_response.json()["recenttracks"]["@attr"]["total"])


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

        for char, replacement in CHAR_AND_REPLACMENT.items():
            input_string.replace(char, replacement)

        return input_string


    @staticmethod
    def rid_of_whitespace(string: str) -> str:
        """Removes leading whitesspace on all lines of a multi-line string"""

        string = "\n".join([line.strip() for line in string.split("\n")])

        return string


    @staticmethod
    def seconds_from_time(input_time: str) -> int:
        """Converts a humanreadable time input into seconds: 4h4s = 14404"""

        time_in_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}
        timeframes = re.findall(r"[0-9]+[smhdwy]", input_time.replace(" ", "").lower())

        return sum(int(timeframe[:-1]) * time_in_seconds[timeframe[-1]] for timeframe in timeframes)