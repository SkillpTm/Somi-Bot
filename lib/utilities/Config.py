import json



class Config():

    with open("config.json", "r") as file:
        configData = json.load(file)

    ACTIVITY_NAME: str = configData["ACTIVITY_NAME"]
    APPLICATION_ID: int = configData["APPLICATION_ID"]
    MAX_MESSAGES_CACHE: int = configData["MAX_MESSAGES_CACHE"]
    POSTGRES_POOL_MAX_SIZE: int = configData["POSTGRES_POOL_MAX_SIZE"]
    OWNER_ID: int = configData["OWNER_ID"]
    VERSION: str = configData["VERSION"]

    BOT_COLOR = int(configData["COLORS"]["BOT"], 16)
    GENIUS_COLOR = int(configData["COLORS"]["GENIUS"], 16)
    LASTFM_COLOR = int(configData["COLORS"]["LASTFM"], 16)
    PERMISSION_COLOR = int(configData["COLORS"]["PERMISSION"], 16)

    HEADS_EMOTE: str = configData["EMOTES"]["HEADS"]
    REACTION_EMOTE: str = configData["EMOTES"]["REACTION"]
    SOMI_BEST_GRILL_EMOTE: str = configData["EMOTES"]["SOMI_BEST_GRILL"]
    SOMI_F_EMOTE: str = configData["EMOTES"]["SOMI_F"]
    SOMI_ONLY_EMOTE: str = configData["EMOTES"]["SOMI_ONLY"]
    SOMI_WELCOME_EMOTE: str = configData["EMOTES"]["SOMI_WELCOME"]
    TAILS_EMOTE: str = configData["EMOTES"]["TAILS"]

    BAN_HAMMER_GIF: str = configData["LINKS"]["BAN_HAMMER_GIF"]
    BOT_GITHUB: str = configData["LINKS"]["BOT_GITHUB"]
    BOT_INVITE: str = configData["LINKS"]["BOT_INVITE"]
    BOT_PP: str = configData["LINKS"]["BOT_PP"]
    BOT_TOS: str = configData["LINKS"]["BOT_TOS"]
    CLOCK_ICON: str = configData["LINKS"]["CLOCK_ICON"]
    DEFAULT_PFP: str = configData["LINKS"]["DEFAULT_PFP"]
    GENIUS_ICON: str = configData["LINKS"]["GENIUS_ICON"]
    LASTFM_ICON: str = configData["LINKS"]["LASTFM_ICON"]
    LINK_EMBED_ICON: str = configData["LINKS"]["LINK_EMBED_ICON"]
    OPENWEATHERMAP_ICON: str = configData["LINKS"]["OPENWEATHERMAP_ICON"]
    SOMI_BEST_GRILL_IMAGE: str = configData["LINKS"]["SOMI_BEST_GRILL_IMAGE"]
    SOMICORD_INVITE: str = configData["LINKS"]["SOMICORD_INVITE"]
    SOMICORD_WELCOME_GIF: str = configData["LINKS"]["SOMICORD_WELCOME_GIF"]
    SPOTIFY_ICON: str = configData["LINKS"]["SPOTIFY_ICON"]

    MODMAIL_SERVER_ID: int = configData["SOMICORD"]["MODMAIL_SERVER_ID"]
    MODMAIL_CHANNEL_ID: int = configData["SOMICORD"]["MODMAIL_CHANNEL_ID"]
    WELCOME_CHANNEL_ID: int = configData["SOMICORD"]["WELCOME_CHANNEL_ID"]

    SUPPORT_SERVER_ID: int = configData["SUPPORT_SERVER"]["ID"]
    SUPPORT_SERVER_ERRORS_ID: int = configData["SUPPORT_SERVER"]["ERRORS_CHANNEL_ID"]
    SUPPORT_SERVER_FEEDBACK_ID: int = configData["SUPPORT_SERVER"]["FEEDBACK_CHANNEL_ID"]
    SUPPORT_SERVER_LOGS_ID: int = configData["SUPPORT_SERVER"]["LOGS_CHANNEL_ID"]