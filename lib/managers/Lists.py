import nextcord

from lib.managers.Singleton import Singleton



class Lists(metaclass=Singleton):

    def __init__(self):

        self.TEXT_CHANNELS = [
            nextcord.ChannelType.text,
            nextcord.ChannelType.news,
            nextcord.ChannelType.public_thread,
            nextcord.ChannelType.news_thread,
            nextcord.ChannelType.private_thread
        ]

        self.LASTFM_TIMEFRAMES = {
            "Past Week": "7day",
            "Past Month": "1month",
            "Past Quarter": "3month",
            "Past Half a Year": "6month",
            "Past Year": "12month",
            "All Time": "overall"
        }

        self.LASTFM_TIMEFRAMES_TEXT = {
            "7day": "of the past week:",
            "1month": "of the past month:",
            "3month": "of the past quarter:",
            "6month": "of the past half a year:",
            "12month": "of the past year:",
            "overall": "of all time:"
        }

        self.LASTFM_TIMEFRAMES_WEBSCRAPING = {
            "Past Week": "LAST_7_DAYS",
            "Past Month": "LAST_30_DAYS",
            "Past Quarter": "LAST_90_DAYS",
            "Past Half a Year": "LAST_180_DAYS",
            "Past Year": "LAST_365_DAYS",
            "All Time": "ALL"
        }

        self.LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT = {
            "LAST_7_DAYS": "Past Week",
            "LAST_30_DAYS": "Past Month",
            "LAST_90_DAYS": "Past Quarter",
            "LAST_180_DAYS": "Past Half a Year",
            "LAST_365_DAYS": "Past Year",
            "ALL": "All Time"
        }

        self.SOMICORD_RULES = {
            "1 NSFW Content": ["No NSFW content is allowed, the only exception of this rule includes sensitive news articles, which have to be marked as a spoiler.", "You spoiler with ||spoiler||."],
            "2 Doxxing": ["Doxxing of users and/or idols is strongly prohibited.", ""],
            "3 Cursing": ["Cursing is allowed, as long, as it is not excessive or is degrading in any way to a specific group of people.", "Excessive is not defined and will be decided case-by-case."],
            "4 Language": ["Use primarily English, if you're asked by a moderator to switch languages, you'll __have__ to switch.", ""],
            "5 Discrimination": ["Racism, discrimination, sexism, ableism, homophobia and any other form of bigotry and prejudice is not allowed.", ""],
            "6 Channel Use": ["Use channels in their intended way, bots can be used in #general, if fitting to the conversation.", ""],
            "7 Unboxing Spoiler Tags": ["Showing off your unboxed kpop content is allowed, as long you spoiler tag the pictures regarding it.", ""],
            "8 Spam": ["Don't excessively use caps, tHiS wAy Of WrItInG, spam emotes, spam pics, spam gifs or spam in general.", ""],
            "9 Negativity": ["Don't bash or talk bad, about any group or artist in general.", "Negativity never made anyone happy, so stay nice."],
            "10 Selfpromotion": ["Self-promotion is prohibited, fanarts are still allowed.", ""],
            "11 Relationships": ["Don't call idols your girlfriend/boyfriend or anything similar. Don't talk about dating them or what you want them to do to you, etc.", ""]
        }