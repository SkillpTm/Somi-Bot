#CHANNELS
AUDIT_LOG_ID = 977261110107439154
MOD_CHANNEL_ID = 992121127159726227
REDDIT_FEED_ID = 1003709719447355512
ROLES_ID = 981636345556512778
WELCOME_CHANNEL_ID = 847221019210809425

MOD_CATEGORY_ID = 1006688054179790949

#ROLES
MODERATOR_ID = 977950744806297620
SOMMUNGCHI_ID = 976833154637766697

#INFO ROLES
UPDATES_ID = 992747153766219826
LIVE_ID = 992747222993215518
SNS_ID = 992747256388272138
REDDIT_ID = 1004420744601686186

#LEVEL ROLES
XOXO_ID = 992767012004700180
WHAT_YOU_WAITING_FOR_ID = 992766911924412467
DUMB_DUMB_ID = 992766967285043260
BIRTHDAY_ID = 992766863874478101
OUTTA_MY_HEAD_ID = 992766793166884865

LEVELROLES = [XOXO_ID,
              WHAT_YOU_WAITING_FOR_ID,
              DUMB_DUMB_ID,
              BIRTHDAY_ID,
              OUTTA_MY_HEAD_ID]

#COLORS

from nextcord import Color

BOT_COLOR = 0xffa6fc
GENIUS_COLOR = 0xf6f069
LASTFM_COLOR = 0xd0232b
MOD_COLOR = Color.blue()
REDDIT_COLOR = 0xfe4600

#REST
BAN_HAMMER_GIF = "https://gfycat.com/bonygiddycoati"
DEFAULT_PFP = "https://cdn.discordapp.com/embed/avatars/0.png"
SOMI_BEST_GRILL_IMAGE = "https://i.imgur.com/65E2MWr.png"
SUBREDDIT_ICON = "https://i.imgur.com/HtTGMwc.gif"
WELCOME_GIF = "https://gfycat.com/partialoblongfreshwatereel"

CLOCK_ICON = "https://i.imgur.com/nqDFTTP.png"
GENIUS_ICON = "https://i.imgur.com/XF1cOBN.png"
LASTFM_ICON = "https://i.imgur.com/a8QaskN.png"
OPENWEATHERMAP_ICON = "https://i.imgur.com/drJnhNn.png"
REDDIT_ICON = "https://i.imgur.com/yXrvhM9.png"
SPOTIFY_ICON = "https://i.imgur.com/YKtWQK4.png"

REACTION_EMOTE = "<a:aSomiBreathTaking:980083399005982801>"
SOMIONLY_EMOTE = "<:SomiONLY:829934613509177354>"
SOMI_F_EMOTE = "<:SomiF:829933531147796510>"
SOMI_BEST_GRILL_EMOTE = "<:SomiBestGrill:924281555772403722>"
HEADS = "<:heads:998363203992031252>"
TAILS = "<:tails:998363225924046949>"

CURRENT_VERSION = "2.1"
SERVER_ID = 769668499605159998
SOMICORD_INVITE = "https://discord.gg/Frd7WYg"

SKILLP_ID = 378214190378123264
SKILLP_JOINED_UNIX_TIME = 1573055760



COMMAND_LIST = """
/about
/avatar
/bam
/choose
/coinflip
/color
/commandlist (alias: /cl)
/custom list
/customcommand (alias: /cc)
/emoji
/feedback
/help
/keyword add
/keyword delete
/keyword list
/kst
/levelroles
/lyrics
/ping
/reminder add
/reminder delete
/reminder list
/serverinfo (alias: /si)
/spotify (alias: /sf)
/somi
/userinfo (alias: ui)
/weather"""

MOD_COMMANDS = """
/ban
/close
/custom add
/custom delete
/edit
/kick
/modcommandlist (alias: /mcl)
/mute
/open
/purge
/reload
/restart
/rules
/send
/shutdown
/slowmode
/unban
/unmute
/vcaccess"""



ROLELIST = {
    UPDATES_ID: "UPDATES",
    LIVE_ID: "LIVE",
    SNS_ID: "SNS",
    REDDIT_ID: "REDDIT"
}



from nextcord import SelectOption

HELP_OPTIONS = [
    SelectOption(label="about", description = "/about"),
    SelectOption(label="avatar", description = "/avatar"),
    SelectOption(label="bam", description = "/bam"),
    SelectOption(label="choose", description = "/choose"),
    SelectOption(label="coinflip", description = "/coinflip"),
    SelectOption(label="color", description = "/color"),
    SelectOption(label="commandlist", description = "/commandlist | /cl"),
    SelectOption(label="custom", description = "/custom list"),
    SelectOption(label="customcommand", description = "/ccustomcommand | /cc"),
    SelectOption(label="emoji", description = "/emoji"),
    SelectOption(label="feedback", description = "/feedback"),
    SelectOption(label="help", description = "/help"),
    SelectOption(label="keyword", description = "/keyword add | /keyword delete | /keyword list"),
    SelectOption(label="kst", description = "/kst"),
    SelectOption(label="levelroles", description = "/levelroles"),
    SelectOption(label="lyrics", description = "/lyrics"),
    SelectOption(label="ping", description = "/ping"),
    SelectOption(label="reminder", description = "/reminder add | /reminder delete | /reminder list"),
    SelectOption(label="serverinfo", description = "/serverinfo | /si"),
    SelectOption(label="spotify", description = "/spotify | /sf"),
    SelectOption(label="somi", description = "/somi"),
    SelectOption(label="userinfo", description = "/userinfo | /ui"),
    SelectOption(label="weather", description = "/weather")
]



HELP_OUTPUT = {
    "about": ["/about (no parameters)\nExample: `/about`",
             f"This command will tell you everything you need to know about the current state of Somi#6418.\nIf you continue to require help please message <@{SKILLP_ID}>"],

    "avatar": [f"/avatar optional[@username]\nExample: `/avatar `<@{SKILLP_ID}>",
               f"This command will post the avatar of the selected user/you.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "bam": ["/bam (no parameters)\nExample: `/bam`",
           f"This command will not actually ban a user. It will just send a mock ban message.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "choose": ["/choose 2-10 Options\nExample: `/choose brown blond black`",
              f"This command randomly chooses between all provided options. You can submit up to 10 options and have to give at least 2 options.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "coinflip": ["/coinflip (no parameters)\nExample: `/coinflip`",
                f"This command gives out either heads or tails.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "color": ["/color [hexcode]\nExample: `/color ffa6fc`",
             f"This command outputs the color coresponding to your hexcode.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "commandlist": ["/commandlist (no parameters) or /cl (no parameters)\nExample: `/commandlist` or `/cl`",
                   f"This command outputs a list with all regular commands.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "custom": ["/custom list (no parameters)\nExample: `/custom list`",
              f"This command will give you a list for all custom command names (You can use these names with `/customcommand`).\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "customcommand": ["/customcommand [custom name] or /cc [custom name]\nExample: `/customcommand somi` or `/cc somi`",
                     f"All custom commands have been created by the moderators and can only be added/removed by a moderator. If you input a custom command name the bot will respond with its output text.\nIf you continue to require further help please message <@{SKILLP_ID}>"],


    "emoji": [f"/emoji [emoji] \nExample: `/emoji `{REACTION_EMOTE}",
             f"This command posts an emoji in its original size.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "feedback": ["/feedback\nExample: `/feedback`",
                f"This command is meant to report bugs/typos/other issues you have encountered while using the bot and any suggestions you have to improve the bot.\nIf you continue to require further help please message <@{SKILLP_ID}>"],      

    "help": ["/help (no parameters)\nExample: `/help`",
            f"This command gives you an explanation for what a certain command does.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "keyword": ["/keyword add [keyword] or delete [keyword] // [ALL] or list\nExample: `/keyword add somi` or `/keyword delete somi` or `/keyword list`",
               f"This command lets you add/delete a keyword to/from your keyword list, which you can open as well. If you set a keyword the bot will send you a direct message when someone else mentions this keyword.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "kst": ["/kst (no parameters)\nExample: `/kst`",
           f"This command tells you the current time in KST (Korean Standard Time).\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "levelroles": ["/levelroles (no parameters)\nExample: `/levelroles`",
                  f"This command will explain the level system of this server to you. It also includes a list of all roles with their levels.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "lyrics": ["/lyrics (no parameters) // optional[Artist] AND optional[Song]\nExample: `/lyrics Jeon Somi XOXO`",
                  f"This command posts the lyrics of the song you are listening to (only if your Spotify is connect to your Discord and you are online) or shows you the lyrics for the specified song.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "ping": ["/ping (no parameters)\nExample: `/ping`",
            f"This command shows you the bot's current ping.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "reminder": ["/reminder add [time] [reminder] or delete [reminder_id] // [ALL] or list\nExample: `/reminder add 5d20h I AM SOMI marathon` or `/remidner delete 0123456789` or `/reminder list`",
                f"This command lets you add or delete a reminder to/from your reminder list, which you can open as well. If you set a reminder the bot will send you a direct message when your defined point of time has happened.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "serverinfo": ["/serverinfo (no parameters) or /si (no parameters)\nExample: `/serverinfo` or `/si`",
                  f"This command gives you information about the server.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "spotify": [f"/spotify optional[@username] or /sf optional[@username]\nExample: `/spotify `<@{SKILLP_ID}> or `/sf `<@{SKILLP_ID}>",
                f"This command tells you what someone is listening to, if their Spotify is connected to Discord and if they are online.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "somi": ["/somi (no parameters)\nExample: `/somi`",
            f"This command will tell you the truth and the truth only.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "userinfo": [f"/userinfo optional[@username] or /ui optional[@username]\nExample: `/userinfo `<@{SKILLP_ID}> or `/ui `<@{SKILLP_ID}>",
                 f"This command will post the user information of the selected user/you.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "weather": [f"/weather [location]\nExample: `/weather Seoul`",
                 f"This command will post the current weather data for the given location.\nIf you continue to require further help please message <@{SKILLP_ID}>"]

}



RULES = {
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