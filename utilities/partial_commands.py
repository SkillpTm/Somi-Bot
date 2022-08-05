###package#import###############################################################################

from datetime import datetime as timedate
import datetime
import humanfriendly
from pytz import timezone
import os
import sys

###self#imports###############################################################################

from utilities.variables import CLOCK_ICON, SKILLP_ID, DEFAULT_PFP, SKILLP_JOINED_UNIX_TIME



###time#related###############################################################################

def embed_kst_footer(embed):
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    try:
        embed.set_footer(text = now_korea.strftime(format), icon_url = CLOCK_ICON)
    except:
        return now_korea, format



def embed_get_user_unix_time(member):
    time1 = datetime.datetime.strptime(str(member.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    
    time2 = datetime.datetime.strptime(str(member.joined_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time2 = datetime.datetime.timestamp(time2)
    
    return int(unix_time1), int(unix_time2)



def embed_get_server_unix_time(interaction):
    time = datetime.datetime.strptime(str(interaction.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time = datetime.datetime.timestamp(time)
    
    return int(unix_time)



def embed_get_member_join_unix_time(member):
    time = datetime.datetime.strptime(str(member.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time = datetime.datetime.timestamp(time)
    
    return int(unix_time)


    
###author#related###############################################################################

def embed_set_message_author(message, embed, title_name):
    try:
        if message.author.avatar is not None:
            embed.set_author(name= title_name, icon_url=message.author.avatar)
        else:
            embed.set_author(name= title_name, icon_url=message.author.default_avatar)
    except:
        if message.user.avatar is not None:
            embed.set_author(name= title_name, icon_url=message.user.avatar)
        else:
            embed.set_author(name= title_name, icon_url=message.user.default_avatar)



def embed_set_mod_author(interaction, embed):
    try:
        if interaction.user.avatar is not None:
            embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
        else:
            embed.set_author(name= "Mod Activity", icon_url=interaction.user.default_avatar)
    except:
        if interaction.avatar is not None:
            embed.set_author(name= "Mod Activity", icon_url=interaction.avatar)
        else:
            embed.set_author(name= "Mod Activity", icon_url=interaction.default_avatar)



def embed_set_somi_author(client, embed):
    if client.user.avatar is not None:
        embed.set_author(name= "Bot Shutdown", icon_url=client.user.avatar)
    else:
        embed.set_author(name= "Bot Shutdown", icon_url=client.user.default_avatar)



def embed_set_server_icon_author(interaction, embed):
    if interaction.guild.icon is not None:
        embed.set_author(name= f"Custom command list for {interaction.guild}", icon_url=interaction.guild.icon)
    else:
        embed.set_author(name= f"Custom command list for {interaction.guild}", icon_url=DEFAULT_PFP)



def embed_get_title_name(member):
    if member.nick != None:
        title_name = member.nick
    else:
        title_name = member.name
    return title_name


        
###thumbnail#related###############################################################################

def embed_set_thumbnail(member, embed):
    if member.avatar is not None:
        embed.set_thumbnail(url=member.avatar)
    else:
        embed.set_thumbnail(url=member.default_avatar)



def embed_set_server_icon(interaction, embed):
    if interaction.guild.icon is not None:
        embed.set_thumbnail(url=interaction.guild.icon)
    else:
        embed.set_thumbnail(url=DEFAULT_PFP)


        
###info#related###############################################################################

from utilities.variables import SERVER_ID

def embed_get_userinfo(member, embed, unix_time1, unix_time2):
    fields = []
    fields += [("ID", member.id, False),
               ("Name:", str(member), True),
               ("Top role", member.top_role.mention, True),
               ("Status", member.status, True),
               ("Created at:", f"<t:{unix_time1}>", True)]

    if member.id == SKILLP_ID and member.guild.id == SERVER_ID:
        fields += [("Joined at:", f"<t:{SKILLP_JOINED_UNIX_TIME}>", True)]
    else:
        fields += [("Joined at:", f"<t:{unix_time2}>", True)]

    fields += [("Boosted", bool(member.premium_since), True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)



def embed_get_serverinfo(interaction, unix_time, embed):
    fields = [("ID:", interaction.guild.id, False),
              ("Members:", len(interaction.guild.members), True),
              ("Owner:", interaction.guild.owner.mention, True),
              ("Channels:", f"{len(interaction.guild.text_channels)} text, {len(interaction.guild.voice_channels)} voice", True),
              ("Created at:", f"<t:{unix_time}>", True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)



###attachment#related###############################################################################

async def embed_attachments(target_channel, message, embed, link_embed = None):
    if link_embed == None:
        link_embed = False
        
        
    if len(message.attachments) == 0:
        await target_channel.send(embed=embed)

    elif len(message.attachments) == 1 or link_embed:
        if "image" in message.attachments[0].content_type:
            embed.set_image(url=message.attachments[0].url)
            
        await target_channel.send(embed=embed)

        if "image" not in message.attachments[0].content_type and not link_embed:
            file = ""
            file += message.attachments[0].url
            await target_channel.send(content=file)

    elif len(message.attachments) > 1 and not link_embed:
        files = ""
        for attachment in range(len(message.attachments)):
            files += f"{message.attachments[attachment].url}\n"
        await target_channel.send(embed=embed)
        await target_channel.send(content=files)



###checks#related###############################################################################

async def is_member_skillp(interaction, member, source):
    if member.id == SKILLP_ID:
        await interaction.response.send_message(f"You can't {source} Skillp!", ephemeral=True)
        return True
    else:
        return False



async def is_member_themself(interaction, member, source):
    if interaction.user == member:
        await interaction.response.send_message(f"You can't {source} yourself!", ephemeral=True)
        return True
    else:
        return False



###time#conversions#related###############################################################################

def time_to_seconds(time):
    total_seconds = 0
    try:
        days = "0d"
        hours = "0h"
        minutes = "0m"
        seconds = "0s"

        clean_time = time.replace(" ", "").lower()

        d_position = clean_time.find("d")
        if d_position > 0:
            days_int = ""
            for i in range(len(clean_time[:d_position])):
                try:
                    int(clean_time[d_position -1 -i])
                    days_int += clean_time[d_position -1 -i]
                except:
                    break
            days = f"{days_int[::-1]}{clean_time[d_position]}"

        h_position = clean_time.find("h")
        if h_position > 0:
            hours_int = ""
            for i in range(len(clean_time[:h_position])):
                try:
                    int(clean_time[h_position -1 -i])
                    hours_int += clean_time[h_position -1 -i]
                except:
                    break
            hours = f"{hours_int[::-1]}{clean_time[h_position]}"

        m_position = clean_time.find("m")
        if m_position > 0:
            minutes_int = ""
            for i in range(len(clean_time[:m_position])):
                try:
                    int(clean_time[m_position -1 -i])
                    minutes_int += clean_time[m_position -1 -i]
                except:
                    break
            minutes = f"{minutes_int[::-1]}{clean_time[m_position]}"

        s_position = clean_time.find("s")
        if s_position > 0:
            seconds_int = ""
            for i in range(len(clean_time[:s_position])):
                try:
                    int(clean_time[s_position -1 -i])
                    seconds_int += clean_time[s_position -1 -i]
                except:
                    break
            seconds = f"{seconds_int[::-1]}{clean_time[s_position]}"

        days_as_seconds = humanfriendly.parse_timespan(days)
        hours_as_seconds = humanfriendly.parse_timespan(hours)
        minutes_as_seconds = humanfriendly.parse_timespan(minutes)
        seconds_as_seconds = humanfriendly.parse_timespan(seconds)

        total_seconds = int(days_as_seconds + hours_as_seconds + minutes_as_seconds + seconds_as_seconds)
    except:
        pass
    return total_seconds



###message#object#related###############################################################################

async def message_object_generation(link, client):
    head, sep, tail = link.partition("https://discord.com/channels/")
    ids_in_link, sep2, tail2 = tail.partition(" ")
    link = sep + ids_in_link
    id_list = ids_in_link.split("/")
    message_id = id_list[2]
    for channel in client.get_all_channels():
        try:
            message = await channel.fetch_message(message_id)
            correct_channel = channel
        except:
            continue
    return message, correct_channel



###reload#custom_command###############################################################################

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


###clean#input#commandname###############################################################################

def make_input_command_clean(commandname):
    remove_characters = [" ", "/"]

    for character in remove_characters:
        commandname = commandname.replace(character, "")

    clean_input = str(commandname.lower())
    return clean_input

###spotify###############################################################################

def get_spotify_track_data(track_spotipy):
    artists_list = []
    artist_urls = []
    i = 0

    while i < len(track_spotipy['artists']):
        artist_urls.append(track_spotipy['artists'][i]['external_urls']['spotify'])
        artists_list.append(track_spotipy['artists'][i]['name'])
        i+=1

    album_url = track_spotipy['album']['external_urls']['spotify']
    album_name = track_spotipy['album']['name']

    track_url = track_spotipy['external_urls']['spotify']
    track_name = track_spotipy['name']

    cover_url = track_spotipy['album']['images'][0]['url']

    return track_url, track_name, album_url, album_name, artist_urls, artists_list, cover_url