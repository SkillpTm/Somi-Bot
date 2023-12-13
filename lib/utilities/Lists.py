####################################################################################################

import nextcord

####################################################################################################

from storage.Config import Config



class Lists():
    SOMI_ID = Config.APPLICATION_ID

    SOMICORD_UPDATE_ROLES_IDS = {
        "UPDATES_ID": Config.UPDATES_ROLE_ID,
        "LIVE_ID": Config.LIVE_ROLE_ID,
        "SNS_ID": Config.SNS_ROLE_ID,
    }



    HELP_AUTOCOMPLETE_TUPLE = (
        "/about",
        "/avatar",
        "/ban",
        "/banner",
        "/choose",
        "/close",
        "/coinflip",
        "/color",
        "/config audit-log-channel",
        "/config default-role",
        "/config hidden-channels",
        "/config info",
        "/config level-ignore-channels",
        "/config level-roles",
        "/custom add",
        "/custom delete",
        "/custom-command",
        "/custom-list",
        "/edit",
        "/emoji",
        "/feedback",
        "/help",
        "/kick",
        "/keyword add",
        "/keyword delete",
        "/keyword list",
        "/kst",
        "/levels info",
        "/levels leaderboard",
        "/levels rank",
        "/lf artist",
        "/lf np",
        "/lf profile",
        "/lf recent",
        "/lf reset",
        "/lf set",
        "/lf topalbums",
        "/lf topartists",
        "/lf toptracks",
        "/lyrics",
        "/mute",
        "/open",
        "/ping",
        "/purge",
        "/reminder add",
        "/reminder delete",
        "/reminder list",
        "/send",
        "/serverinfo",
        "/slowmode",
        "/spotify",
        "/somi",
        "/unban",
        "/unmute",
        "/userinfo",
        "/vc-access",
        "/weather",
        "/wolfram",
        "/youtube",
    )


    HELP_NORMAL_OUTPUT = {
        "/about": [
            """
            ```/about (no parameters)```
            """,
            "/about"
        ],

        "/avatar": [
            """
            ```/avatar optional[@USERNAME]```
            `@USERNAME`:
            A user on this server.
            Default: you
            """,
            f"/avatar [<@{SOMI_ID}>]"
        ],

        "/bam": [
            """
            ```/bam (no parameters)```
            """,
            "/bam"
        ],

        "/banner": [
            """
            ```/banner optional[@USERNAME]```
            `@USERNAME`:
            A user on this server.
            Default: you
            """,
            f"/banner [<@{SOMI_ID}>]"
        ],

        "/choose": [
            """
            ```/choose [option 1] [option 2] optional[3-10 options]```
            `option 1-10`:
            Any input to be choosen between.
            Default: nothing
            Length requirments: 1-200 characters

            (note: The command 'choose' has a search shortend as 'select'.)
            """,
            "/choose [brown] [blond] [black]"
        ],

        "/coinflip": [
            """
            ```/coinflip (no parameters)```
            """,
            "/coinflip"
        ],

        "/color": [
            """
            ```/color [hexcode]```
            `hexcode`:
            A valid hexcode for a color. This hexcode can, but doesn't have, to start with a '#'.
            Length requirments: 6-7 characters
            """,
            "/color [#ffa6fc]"
        ],

        "/custom-command": [
            """
            ```/custom-command [commandname]```
            `commandname`:
            The name of the custom-command.
            Restrictions: Can only consist of letters and numbers
            Length requirments: 2-50 characters

            (note: The command 'custom-command' has a search shortend as 'cc'.)
            """,
            "/custom-command [number1]"
        ],

        "/custom-list": [
            """
            ```/custom-list (no parameters)```

            (note: The command 'custom-list' has a search shortend as 'cl'.)
            """,
            "/custom-list"
        ],

        "/emoji": [
            """
            ```/emoji [:EMOJINAME:]```
            `:EMOJINAME:`:
            A custom server emoji from any server.
            Length requirments: 2-100 characters
            """,
            "/emoji [:SomiBestGrill:]"
        ],

        "/feedback": [
            """
            ```/feedback (no parameters)```
            """,
            "/feedback"
        ],

        "/help": [
            """
            ```/help [commandname]```
            `commandname`:
            The commandname for which you require help.
            """,
            "/help [/help]"
        ],

        "/keyword add": [
            """
            ```/keyword add [keyword]```
            `keyword`:
            The keyword to be notified about.
            Restrictions: Can only consist of letters and numbers
            Length requirments: 2-50 characters

            (note: The command 'keyword' has a search shortend as 'noti'.)
            """,
            "/keyword add [Somi]"
        ],

        "/keyword delete": [
            """
            ```/keyword delete [keyword]```
            `keyword`:
            The keyword to be notified about. (note: By inputing 'ALL' in caps you can get a special option to delete all of your keywords at once.)
            Restrictions: Can only consist of letters and numbers
            Length requirments: 2-50 characters

            (note: The command 'keyword' has a search shortend as 'noti'.)
            """,
            "/keyword delete [Somi]"
        ],

        "/keyword list": [
            """
            ```/keyword list (no parameters)```

            (note: The command 'keyword' has a search shortend as 'noti'.)
            """,
            "/keyword list"
        ],

        "/kst": [
            """
            ```/kst (no parameters)```
            """,
            "/kst"
        ],

        "/levels info": [
            """
            ```/levels info (no parameters)```
            """,
            "/levels info"
        ],

        "/levels leaderboard": [
            """
            ```/levels leaderboard (no parameters)```

            (note: The subcommand 'leaderboard' has a search shortend as 'top'.)
            """,
            "/levels leaderboard"
        ],

        "/levels rank": [
            """
            ```/levels rank optional[@USERNAME]```
            `@USERNAME`:
            A user on this server.
            Default: you
            """,
            f"/levels rank [<@{SOMI_ID}>]"
        ],

        "/lf artist": [
            """
            ```/lf artist optional[artist] optional[@USERNAME] optional[timeframe]```
            `artist`:
            An artist who exists with this __exact__ name on LastFm.
            Default: If you have a LastFm account connected to Somi this will default to what you're playing right now or to what you last listened to.
            Length requirments: 2-100 characters

            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'
            """,
            f"/lf artist [Jeon Somi] [<@{SOMI_ID}>] [Past Week]"
        ],

        "/lf album": [
            """
            ```/lf album optional[artist] optional[album] optional[@USERNAME] optional[timeframe]```
            `artist`:
            An artist who exists with this __exact__ name on LastFm.
            Default: If you have a LastFm account connected to Somi this will default to what you're playing right now or to what you last listened to.
            Length requirments: 2-100 characters

            `album`:
            An album which exists with this __exact__ name on LastFm.
            Default: If you have a LastFm account connected to Somi this will default to what you're playing right now or to what you last listened to.
            Length requirments: 2-100 characters

            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'
            """,
            f"/lf album [Jeon Somi] [XOXO] [<@{SOMI_ID}>] [Past Week]"
        ],

        "/lf np": [
            """
            ```/lf np optional[@USERNAME]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            (note: The subcommand 'np' has a search shortend as 'nowplaying'.)
            """,
            f"/lf np [<@{SOMI_ID}>]"
        ],

        "/lf profile": [
            """
            ```/lf profile optional[@USERNAME]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you
            """,
            f"/lf profile [<@{SOMI_ID}>]"
        ],

        "/lf recent": [
            """
            ```/lf recent optional[@USERNAME]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            (note: The subcommand 'recent' has a search shortend as 'rc'.)
            """,
            f"/lf recent [<@{SOMI_ID}>]"
        ],

        "/lf set": [
            """
            ```/lf set [lastfmname]```
            `lastfmname`:
            Your LastFm username, this name will have to __exactly__ match your username on LastFm.
            Length requirments: 2-100 characters
            """,
            "/lf set [SomiBot]"
        ],

        "/lf reset": [
            """
            ```/lf reset (no parameters)```
            """,
            "/lf reset"
        ],

        "/lf topalbums": [
            """
            ```/lf topalbums optional[@USERNAME] optional[timeframe]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'

            (note: The subcommand 'topalbums' has a search shortend as 'tal'.)
            """,
            f"/lf topalbums [<@{SOMI_ID}>] [Past Month]"
        ],

        "/lf topartists": [
            """
            ```/lf topartists optional[@USERNAME] optional[timeframe]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'

            (note: The subcommand 'topartists' has a search shortend as 'tar'.)
            """,
            f"/lf topartists [<@{SOMI_ID}>] [Past Quarter]"
        ],

        "/lf toptracks": [
            """
            ```/lf toptracks optional[@USERNAME] optional[timeframe]```
            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'

            (note: The subcommand 'toptracks' has a search shortend as 'tt'.)
            """,
            f"/lf toptracks [<@{SOMI_ID}>] [Past Half a Year]"
        ],

        "/lf track": [
            """
            ```/lf track optional[artist] optional[track] optional[@USERNAME] optional[timeframe]```
            `artist`:
            An artist who exists with this __exact__ name on LastFm.
            Default: If you have a LastFm account connected to Somi this will default to what you're playing right now or to what you last listened to.
            Length requirments: 2-100 characters

            `track`:
            A track which exists with this __exact__ name on LastFm.
            Default: If you have a LastFm account connected to Somi this will default to what you're playing right now or to what you last listened to.
            Length requirments: 2-100 characters

            `@USERNAME`:
            A user on this server, who has a LastFm account connected to Somi.
            Default: you

            `timeframe`:
            A preset timeframe that will limit from when on to gather data.
            Default: 'All Time'
            """,
            f"/lf track [Jeon Somi] [XOXO] [<@{SOMI_ID}>] [Past Week]"
        ],

        "/lyrics": [
            """
            ```/lyrics optional[artist] optional[song]```
            `artist`:
            The artist of the song.
            Default: What you are listening to on Spotify, if your Spotify is publically connected to Discord.
            Length requirments: 2-100 characters

            `song`:
            The name of the song.
            Default: What you are listening to on Spotify, if your Spotify is publically connected to Discord.
            Length requirments: 2-100 characters

            (note: The command 'lyrics' has a search shortend as 'genius'.)
            """,
            "/lf lyrics [Jeon Somi] [XOXO]"
        ],

        "/ping": [
            """
            ```/ping (no parameters)```
            """,
            "/ping"
        ],

        "/reminder add": [
            """
            ```/reminder add [time] [reminder]```
            `time`:
            The time in which you're supposed to get reminded.
            Restrictions: Can only follow a pattern of chaininig timeframes with a number and then y, w, d, h, m or s. The combined time has to be smaller than 10 years.
            Length requirments: 1-50 characters

            `reminder`:
            The thing you want to be reminded about.
            Length requirments: 1-4096 characters

            (note: The command 'reminder' has a search shortend as 'alarm'.)
            """,
            "/reminder add [12w 4d 6h] [Somi comeback with a full album of 20 tracks.]"
        ],

        "/reminder delete": [
            """
            ```/reminder add [reminder id]```
            `reminder id`:
            The id of the reminder you wish to delete. (note: By inputing 'ALL' in caps you can get a special option to delete all of your reminders at once.)
            Length requirments: 1-10 numbers

            (note: The command 'reminder' has a search shortend as 'alarm'.)
            """,
            "/reminder delete [2001030900]"
        ],

        "/reminder list": [
            """
            ```/reminder list (no parameters)```

            (note: The command 'reminder' has a search shortend as 'alarm'.)
            """,
            "/reminder list"
        ],

        "/serverinfo": [
            """
            ```/serverinfo (no parameters)```

            (note: The command 'serverinfo' has a search shortend as 'si'.)
            """,
            "/serverinfo",
        ],

        "/somi": [
            """
            ```/somi (no parameters)```
            """,
            "/somi",
        ],

        "/spotify": [
            """
            ```/spotify optional[@USERNAME]```
            `@USERNAME`:
            A user on this server, who has their Spotify publically connected to Discord.
            Default: you

            (note: The command 'sporify' has a search shortend as 'sf'.)
            """,
            "/somi",
        ],

        "/userinfo": [
            """
            ```/userinfo optional[@USERNAME]```
            `@USERNAME`:
            A user on this server, who has their Spotify publically connected to Discord.
            Default: you

            (note: The command 'userinfo' has a search shortend as 'ui'.)
            """,
            f"/userinfo [<@{SOMI_ID}>]",
        ],

        "/weather": [
            """
            ```/weather [location]```
            `location`:
            A location that can be found in OpenWeatherMap's database.
            Length requirments: 2-50
            """,
            "/weather [Seoul]",
        ],

        "/wolfram": [
            """
            ```/wolfram [query]```
            `query`:
            A query that can be asked to the Wolfram service.
            Length requirments: 2-200
            """,
            "/wolfram [What is 20C° in Fahrenheit?]",
        ],

        "/youtube": [
            """
            ```/youtube [query]```
            `query`:
            A query for what video to find on YouTube.
            Length requirments: 2-200

            (note: The command 'youtube' has a search shortend as 'yt'.)
            """,
            "/youtube [Jeon Somi XOXO MV]",
        ]
    }



    HELP_PERMISSION_OUTPUT = {
        "/ban": [
            """
            ```/ban [@USERNAME] optional[message delete hours] optional[reason]```
            `@USERNAME`:
            A user on this server.

            `message delete hours`:
            The amount of hours for which this user's past messages will be deleted. To not delete any messages input 0.
            Default: 1
            Length requirments: 0-168

            `reason`:
            The reason for why this user was banned. (note: The user will get a pm with this reason.)
            Default: nothing
            Length requirments: 2-1000 characters
            """,
            f"/ban [<@{SOMI_ID}>] [24] [Use of bigotry terms in a harmful way.]",
            "ban members: ✅"
        ],

        "/close": [
            """
            ```/close (no parameters)```

            (note: For this command to work you need to set a default-role with `/config default-role`.)
            """,
            "/close",
            "manage roles: ✅\nmanage guild: ✅"
        ],

        "/config audit-log-channel": [
            """
            ```/config audit-log-channel [action] optional[#CHANNELNAME]```
            `action`:
            This defines if you want to set a new channel or unset the current channel. You don't need to unset the current channel to set a new channel.

            `#CHANNELNAME`:
            A channel on this server. (A channel in this context is a: text-channel, news-channel or thread of any kind)
            Default: current channel (if the action is set)

            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config audit-log-channel [Set] [#audit-log]",
            "manage guild: ✅"
        ],

        "/config default-role": [
            """
            ```/config default-role [action] optional[@ROLENAME]```
            `action`:
            This defines if you want to set a new role or unset the current role. You don't need to unset the current role to set a new role.

            `@ROLENAME`:
            A role on this server. (note: In order for Somi to apply this role, her role needs to be placed above this role.)

            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config default-role [Set] [@Member]",
            "manage guild: ✅"
        ],

        "/config hidden-channels": [
            """
            ```/config hidden-channels [action] optional[#CHANNELNAME]```
            `action`:
            This defines if you want to add or remove a channel.

            `#CHANNELNAME`:
            A channel on this server. (A channel in this context is a: text-channel, news-channel or thread of any kind)
            Default: current channel

            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config default-role [Add] [#general]",
            "manage guild: ✅"
        ],

        "/config info": [
            """
            ```/config info (no parameters)```

            (note: In order for Somi to properly execute some config commands her role needs to be above all roles she is supposed to manage.)
            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config info",
            "manage guild: ✅"
        ],

        "/config level-ignore-channels": [
            """
            ```/config level-ignore-channels [action] optional[#CHANNELNAME]```
            `action`:
            This defines if you want to add or remove a channel.

            `#CHANNELNAME`:
            A channel on this server. (A channel in this context is a: text-channel, news-channel or thread of any kind)
            Default: current channel

            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config level-ignore-channels [Add] [#bot-channel]",
            "manage guild: ✅"
        ],

        "/config level-roles": [
            """
            ```/config level-roles [action] [@ROLENAME] optional[level]```
            `action`:
            This defines if you want to add or remove a role.

            `@ROLENAME`:
            A role on this server. (note: In order for Somi to apply this role, her role needs to be placed above this role.)

            `level`:
            The level you want a new level-role to be applied from.
            Length requirments: 1-1000

            (note: The command 'config' has a search shortend as 'manage'.)
            """,
            "/config level-roles [Add] [@active-community-member] [20]",
            "manage guild: ✅"
        ],

        "/custom add": [
            """
            ```/custom add [commandname] [commandtext]```
            `commandname`:
            The name of the custom-command.
            Restrictions: Can only consist of letters and numbers
            Length requirments: 2-50 characters

            `commandtext`:
            This is what will later be output by the bot when this custom-command is selected.
            Length requirments: 2-1000 characters
            """,
            "/custom add [number1] [Somi is the nummber 1!]",
            "manage messages: ✅\nmanage guild: ✅"
        ],

        "/custom delete": [
            """
            ```/custom delete [commandname]```
            `commandname`:
            The name of the custom-command.
            Restrictions: Can only consist of letters and numbers
            Length requirments: 2-50 characters
            """,
            "/custom delete [number1]",
            "manage messages: ✅\nmanage guild: ✅"
        ],

        "/edit": [
            """
            ```/edit [message id] [message]```
            `message id`:
            The message id of a message previously sent by the bot.
            Length requirments: 18-19 characters

            `message`:
            The new text of the message to be edited.
            Length requirments: 1-1000 characters
            """,
            "/edit [1053475874592264262] [Somi is best grill.]",
            "manage messages: ✅"
        ],

        "/kick": [
            """
            ```/kick [@USERNAME] optional[reason]```
            `@USERNAME`:
            A user on this server.

            `reason`:
            The reason for why this user was kicked. (note: The user will get a pm with this reason.)
            Default: nothing
            Length requirments: 2-1000 characters
            """,
            f"/kick [<@{SOMI_ID}>] [Keeps being annoying to staff and asking for a moderator role.]",
            "kick members: ✅"
        ],

        "/mute": [
            """
            ```/mute [@USERNAME] [time] optional[reason]```
            `@USERNAME`:
            A user on this server.

            `time`:
            The time for which the user is supossed to get muted.
            Restrictions: Can only follow a pattern of chaininig timeframes with a number and then w, d, h, m or s. The combined time has to be smaller than 28 days.
            Length requirments: 2-50 characters

            `reason`:
            The reason for why this user was muted. (note: The user will __not__ get a pm with this reason, it exists only for the audit-log message.)
            Default: nothing
            Length requirments: 2-1000 characters
            """,
            f"/mute [<@{SOMI_ID}>] [1d 3h 55m 20s] [Insulted another member.]",
            "mute members: ✅"
        ],

        "/open": [
            """
            ```/open (no parameters)```

            (note: For this command to work you need to set a default-role with `/config default-role`.)
            (note: The command 'open' has a search shortend as 'unclose'.)
            """,
            "/open",
            "manage roles: ✅\nmanage guild: ✅"
        ],

        "/purge": [
            """
            ```/purge [amount]```
            `amount`:
            The amount fo messages you want to delete.
            Length requirments: 1-1000

            (note: The command 'purge' has a search shortend as 'clear'.)
            """,
            "/open",
            "manage messages: ✅"
        ],

        "/send": [
            """
            ```/send [message] optional[#CHANNELNAME]```
            `message`:
            The new text of the message to be sent.
            Length requirments: 2-1000 characters

            `#CHANNELNAME`:
            A channel on this server. (A channel in this context is a: text-channel, news-channel or thread of any kind)
            Default: current channel

            (note: The command 'send' has a search shortend as 'say'.)
            """,
            "/send [Somi is best grill.] [#general]",
            "manage messages: ✅"
        ],

        "/slowmode": [
            """
            ```/slowmode [delay] optional[#CHANNELNAME]```
            `delay`:
            The delay between new messages per user. To turn slowmode off again input 0. (note: You're not effected by slowmode, if you have the manage channels or manage messages permission.)
            Length requirments: 0-21600 characters

            `#CHANNELNAME`:
            A channel on this server. (A channel in this context is a: text-channel, news-channel or thread of any kind)
            Default: current channel
            """,
            "/send [Somi is best grill.] [#general]",
            "manage channels: ✅"
        ],

        "/unban": [
            """
            ```/unban [user id]```
            `user_id`:
            The user id of a user who has been banned from this server.
            Length requirments: 18-19 numbers
            """,
            f"/unban [{SOMI_ID}]",
            "ban members: ✅"
        ],

        "/unmute": [
            """
            ```/unmute [@USERNAME]```
            `@USERNAME`:
            A user on this server.
            """,
            f"/unmute [<@{SOMI_ID}>]",
            "mute members: ✅"
        ],

        "/vc-access": [
            """
            ```/vc-access [action] [@USERNAME]```
            `action`:
            This defines if you want to allows or forbid access to the user.

            `@USERNAME`:
            A user on this server.
            """,
            f"/vc-access [Forbid] [<@{SOMI_ID}>]",
            "manage channels: ✅"
        ],
    }



    SOMICORD_RULES = {
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