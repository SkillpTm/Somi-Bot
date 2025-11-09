import json

from lib.managers.Singleton import Singleton



class Config(metaclass=Singleton):
    """Holds all the config.json and ISOCountryTags.json data on it"""

    def __init__(self):
        with open("./assets/res/ISOCountryTags.json", "r", encoding="UTF-8") as file:
            iso_data = json.load(file)

        self.ISO_COUNTRY_TAGS: dict[str, str] = iso_data

        with open("./config.json", "r", encoding="UTF-8") as file:
            config_data = json.load(file)

        # Meta values
        self.ACTIVITY_NAME: str = config_data["ACTIVITY_NAME"]
        self.APPLICATION_BANNER_PATH: str = config_data["APPLICATION_BANNER_PATH"]
        self.APPLICATION_ICON_PATH: str = config_data["APPLICATION_ICON_PATH"]
        self.APPLICATION_ID: int = config_data["APPLICATION_ID"]
        self.APPLICATION_NAME: str = config_data["APPLICATION_NAME"]
        self.MAX_MESSAGES_CACHE: int = config_data["MAX_MESSAGES_CACHE"]
        self.POSTGRES_POOL_MAX_SIZE: int = config_data["POSTGRES_POOL_MAX_SIZE"]
        self.OWNER_ID: int = config_data["OWNER_ID"]
        self.VERSION: str = config_data["VERSION"]

        # Colors
        self.BOT_COLOR = int(config_data["COLORS"]["BOT"], 16)
        self.GENIUS_COLOR = int(config_data["COLORS"]["GENIUS"], 16)
        self.LASTFM_COLOR = int(config_data["COLORS"]["LASTFM"], 16)
        self.PERMISSION_COLOR = int(config_data["COLORS"]["PERMISSION"], 16)

        # Emotes
        self.HEADS_EMOTE: str = config_data["EMOTES"]["HEADS"]
        self.REACTION_EMOTE: str = config_data["EMOTES"]["REACTION"]
        self.SOMI_BEST_GRILL_EMOTE: str = config_data["EMOTES"]["SOMI_BEST_GRILL"]
        self.SOMI_F_EMOTE: str = config_data["EMOTES"]["SOMI_F"]
        self.SOMI_ONLY_EMOTE: str = config_data["EMOTES"]["SOMI_ONLY"]
        self.SOMI_WELCOME_EMOTE: str = config_data["EMOTES"]["SOMI_WELCOME"]
        self.TAILS_EMOTE: str = config_data["EMOTES"]["TAILS"]

        # Links
        self.BAN_HAMMER_GIF: str = config_data["LINKS"]["BAN_HAMMER_GIF"]
        self.BOT_GITHUB: str = config_data["LINKS"]["BOT_GITHUB"]
        self.BOT_INVITE: str = config_data["LINKS"]["BOT_INVITE"]
        self.BOT_PP: str = config_data["LINKS"]["BOT_PP"]
        self.BOT_TOS: str = config_data["LINKS"]["BOT_TOS"]
        self.CLOCK_ICON: str = config_data["LINKS"]["CLOCK_ICON"]
        self.DEFAULT_PFP: str = config_data["LINKS"]["DEFAULT_PFP"]
        self.GENIUS_ICON: str = config_data["LINKS"]["GENIUS_ICON"]
        self.HEADPHONES_ICON: str = config_data["LINKS"]["HEADPHONES_ICON"]
        self.LASTFM_ICON: str = config_data["LINKS"]["LASTFM_ICON"]
        self.LINK_EMBED_ICON: str = config_data["LINKS"]["LINK_EMBED_ICON"]
        self.OPENWEATHERMAP_ICON: str = config_data["LINKS"]["OPENWEATHERMAP_ICON"]
        self.SOMI_BEST_GRILL_IMAGE: str = config_data["LINKS"]["SOMI_BEST_GRILL_IMAGE"]
        self.SOMICORD_INVITE: str = config_data["LINKS"]["SOMICORD_INVITE"]
        self.SOMICORD_WELCOME_GIF: str = config_data["LINKS"]["SOMICORD_WELCOME_GIF"]
        self.SPOTIFY_ICON: str = config_data["LINKS"]["SPOTIFY_ICON"]
        self.SUPPORT_SERVER_INVITE: str = config_data["LINKS"]["SUPPORT_SERVER_INVITE"]

        # Somicord related values
        self.MODMAIL_SERVER_ID: int = config_data["SOMICORD"]["MODMAIL_SERVER_ID"]
        self.MODMAIL_CHANNEL_ID: int = config_data["SOMICORD"]["MODMAIL_CHANNEL_ID"]
        self.WELCOME_CHANNEL_ID: int = config_data["SOMICORD"]["WELCOME_CHANNEL_ID"]

        # Support server related values
        self.SUPPORT_SERVER_ID: int = config_data["SUPPORT_SERVER"]["ID"]
        self.SUPPORT_SERVER_ERRORS_ID: int = config_data["SUPPORT_SERVER"]["ERRORS_CHANNEL_ID"]
        self.SUPPORT_SERVER_FEEDBACK_ID: int = config_data["SUPPORT_SERVER"]["FEEDBACK_CHANNEL_ID"]
        self.SUPPORT_SERVER_LOGS_ID: int = config_data["SUPPORT_SERVER"]["LOGS_CHANNEL_ID"]