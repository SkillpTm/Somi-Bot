import json



class Config():

    with open('config.json', 'r') as file:
        configData = json.load(file)

    APPLICATION_ID = configData["APPLICATION_ID"]
    OWNER_ID = configData["OWNER_ID"]
    POSTGRES_POOL_MAX_SIZE = configData["POSTGRES_POOL_MAX_SIZE"]

    SUPPORT_SERVER_ID = configData["SUPPORT_SERVER"]["ID"]
    SUPPORT_SERVER_LOGS_ID = configData["SUPPORT_SERVER"]["LOGS_CHANNEL_ID"]
    SUPPORT_SERVER_FEEDBACK_ID = configData["SUPPORT_SERVER"]["FEEDBACK_CHANNEL_ID"]

    MODMAIL_SERVER_ID = configData["SOMICORD"]["MODMAIL_SERVER_ID"]
    MODMAIL_CHANNEL_ID = configData["SOMICORD"]["MODMAIL_CHANNEL_ID"]
    WELCOME_CHANNEL_ID = configData["SOMICORD"]["WELCOME_CHANNEL_ID"]

    HEADS_EMOTE = configData["EMOTES"]["HEADS"]
    REACTION_EMOTE = configData["EMOTES"]["REACTION"]
    SOMI_BEST_GRILL_EMOTE = configData["EMOTES"]["SOMI_BEST_GRILL"]
    SOMI_F_EMOTE = configData["EMOTES"]["SOMI_F"]
    SOMI_ONLY_EMOTE = configData["EMOTES"]["SOMI_ONLY"]
    SOMI_WELCOME_EMOTE = configData["EMOTES"]["SOMI_WELCOME"]
    TAILS_EMOTE = configData["EMOTES"]["TAILS"]