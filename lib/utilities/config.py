####################################################################################################

import nextcord

####################################################################################################



TEXT_CHANNELS = [
    nextcord.ChannelType.text,
    nextcord.ChannelType.news,
    nextcord.ChannelType.public_thread,
    nextcord.ChannelType.news_thread,
    nextcord.ChannelType.private_thread
]

LASTFM_TIMEFRAMES = {
    "Past Week": "7day",
    "Past Month": "1month",
    "Past Quarter": "3month",
    "Past Half a Year": "6month",
    "Past Year": "12month",
    "All Time": "overall"
}

LASTFM_TIMEFRAMES_TEXT = {
    "7day": "of the past week:",
    "1month": "of the past month:",
    "3month": "of the past quarter:",
    "6month": "of the past half a year:",
    "12month": "of the past year:",
    "overall": "of all time:"
}

LASTFM_TIMEFRAMES_WEBSCRAPING = {
    "Past Week": "LAST_7_DAYS",
    "Past Month": "LAST_30_DAYS",
    "Past Quarter": "LAST_90_DAYS",
    "Past Half a Year": "LAST_180_DAYS",
    "Past Year": "LAST_365_DAYS",
    "All Time": "ALL"
}

LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT = {
    "LAST_7_DAYS": "Past Week",
    "LAST_30_DAYS": "Past Month",
    "LAST_90_DAYS": "Past Quarter",
    "LAST_180_DAYS": "Past Half a Year",
    "LAST_365_DAYS": "Past Year",
    "ALL": "All Time"
}