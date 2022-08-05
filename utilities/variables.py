#CHANNELS
AUDIT_LOG_ID = 977261110107439154
MOD_CHANNEL_ID = 992121127159726227
MOD_BOT_ID = 562987593801793556
MOD_CORD_LOG_ID = 898969582608478209
REDDIT_FEED_ID = 1003709719447355512
ROLES_ID = 981636345556512778
WELCOME_CHANNEL_ID = 847221019210809425

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
REDDIT_ICON = "https://i.imgur.com/yXrvhM9.png"
SPOTIFY_ICON = "https://i.imgur.com/YKtWQK4.png"

REACTION_EMOTE = "<a:aSomiBreathTaking:980083399005982801>"
SOMIONLY_EMOTE = "<:SomiONLY:829934613509177354>"
SOMI_F = "<:SomiF:829933531147796510>"
HEADS = "<:heads:998363203992031252>"
TAILS = "<:tails:998363225924046949>"

CURRENT_VERSION = "1.2"
SERVER_ID = 769668499605159998
SOMICORD_INVITE = "https://discord.gg/Frd7WYg"

SKILLP_ID = 378214190378123264
SKILLP_JOINED_UNIX_TIME = 1573055760



COMMAND_LIST = """
/about
/avatar
/bam
/bugs
/choose
/coinflip
/commandlist (alias: /cl)
/custom list
/customcommand (alias: /cc)
/emoji
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
/suggestions
/userinfo (alias: ui)"""

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
/send
/shutdown
/unban
/unmute
/vcaccess"""



EXTENSION_FOLDERS = [
    "_global_data",
    "command_overview",
    "custom",
    "info",
    "keywords",
    "logs",
    "mod_commands",
    "modmail",
    "music",
    "reminders",
    "role_selection",
    "simple",
    "text_response",
    "user_submissions",
    "voicechannel"]



ROLELIST = {
    UPDATES_ID: "UPDATES",
    LIVE_ID: "LIVE",
    SNS_ID: "SNS",
    REDDIT_ID: "REDDIT"
}



MOD_CHANNELS = {
    "AUDIT_LOG": AUDIT_LOG_ID,
    "MOD_CHANNEL": MOD_CHANNEL_ID,
    "MOD_BOT": MOD_BOT_ID,
    "MOD_CORD_LOG": MOD_CORD_LOG_ID
}



import nextcord

HELP_OPTIONS = [
    nextcord.SelectOption(label="about", description = "/about"),
    nextcord.SelectOption(label="avatar", description = "/avatar"),
    nextcord.SelectOption(label="bam", description = "/bam"),
    nextcord.SelectOption(label="bugs", description = "/bugs"),
    nextcord.SelectOption(label="choose", description = "/choose"),
    nextcord.SelectOption(label="coinflip", description = "/coinflip"),
    nextcord.SelectOption(label="commandlist", description = "/commandlist | /cl"),
    nextcord.SelectOption(label="custom", description = "/custom list"),
    nextcord.SelectOption(label="customcommand", description = "/ccustomcommand | /cc"),
    nextcord.SelectOption(label="emoji", description = "/emoji"),
    nextcord.SelectOption(label="help", description = "/help"),
    nextcord.SelectOption(label="keyword", description = "/keyword add | /keyword delete | /keyword list"),
    nextcord.SelectOption(label="kst", description = "/kst"),
    nextcord.SelectOption(label="levelroles", description = "/levelroles"),
    nextcord.SelectOption(label="lyrics", description = "/lyrics"),
    nextcord.SelectOption(label="ping", description = "/ping"),
    nextcord.SelectOption(label="reminder", description = "/reminder add | /reminder delete | /reminder list"),
    nextcord.SelectOption(label="serverinfo", description = "/serverinfo | /si"),
    nextcord.SelectOption(label="spotify", description = "/spotify | /sf"),
    nextcord.SelectOption(label="somi", description = "/somi"),
    nextcord.SelectOption(label="suggestions", description = "/suggestions"),
    nextcord.SelectOption(label="userinfo", description = "/userinfo | /ui")
]



HELP_OUTPUT = {
    "about": ["/about (no parameters)\nExample: `/about`",
             f"This command will tell you everything you need to know about the current state of Somi#6418.\nIf you continue to require help please message <@{SKILLP_ID}>"],

    "avatar": [f"/avatar optional[@username]\nExample: `/avatar `<@{SKILLP_ID}>",
               f"This command will post the avatar of the selected user/you.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "bam": ["/bam (no parameters)\nExample: `/bam`",
           f"This command will not actually ban a user. It will just send a mock ban message.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "bugs": ["/bugs (no parameters)\nExample: `/bugs`",
            f"This command is meant to report bugs/typos/other issues you have encountered while using the bot. Be aware that, if you use this command your bug report, together with your ID and name will be stored in a database. You can add that you want to be informed, as soon as the problem has been fixed.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "choose": ["/choose 2-10 Options\nExample: `/choose brown blond black`",
              f"This command randomly chooses between all provided options. You can submit up to 10 options and have to give at least 2 options.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "coinflip": ["/coinflip (no parameters)\nExample: `/coinflip`",
                f"This command gives out either heads or tails.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "commandlist": ["/commandlist (no parameters) or /cl (no parameters)\nExample: `/commandlist` or `/cl`",
                   f"This command outputs a list with all regular commands.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "customcommand": ["/customcommand [custom name] or /cc [custom name]\nExample: `/customcommand somi` or `/cc somi`",
                     f"All custom commands have been created by the moderators and can only be added/removed by a moderator. If you input a custom command name the bot will respond with its output text.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "custom": ["/custom list (no parameters)\nExample: `/custom list`",
              f"This command will give you a list for all custom command names (You can use these names with `/customcommand`.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "emoji": [f"/emoji [emoji] \nExample: `/emoji `{REACTION_EMOTE}",
             f"This command posts an emoji in its original size.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "help": ["/help (no parameters)\nExample: `/help`",
            f"This command gives you an explanation for what a certain command does.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "keyword": ["/keyword add [keyword] or delete [keyword] // [ALL] or list\nExample: `/keyword add somi` or `/keyword delete somi` or `/keyword list`",
               f"This command lets you add or delete a keyword to your keyword list, which you can open as well. If you set a keyword the bot will send you a direct message when someone else mentions this keyword.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "kst": ["/kst (no parameters)\nExample: `/kst`",
           f"This command tells you the current time in KST (Korean Standard Time).\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "levelroles": ["/levelroles (no parameters)\nExample: `/levelroles`",
                  f"This command will explain the level system of this server to you. It also includes a list of all roles with levels.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "lyrics": ["/lyrics (no parameters) // [Artist] AND [Song]\nExample: `/lyrics Jeon Somi XOXO`",
                  f"This command posts to lyrics of the song you are listening to (only if your Spotify is connect to your Discord and you are online) or shows you the lyrics for the specified song.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

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

    "suggestions": ["/suggestions (no parameters)\nExample: `/suggestions`",
                   f"This command is meant to give suggestions for the bot. Be aware that, if you use this command your suggestion, together with your ID and name will be stored in a database. You can add that you want to be informed, about what is going to happen regarding your suggestion.\nIf you continue to require further help please message <@{SKILLP_ID}>"],

    "userinfo": [f"/userinfo optional[@username] or /ui optional[@username]\nExample: `/userinfo `<@{SKILLP_ID}> or `/ui `<@{SKILLP_ID}>",
                 f"This command will post the user information of the selected user/you.\nIf you continue to require further help please message <@{SKILLP_ID}>"]
}