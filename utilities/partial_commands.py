###package#import###############################################################################

from datetime import datetime as timedate
import datetime
import humanfriendly
from pytz import timezone
import os
import sys

###self#imports###############################################################################

from utilities.variables import BOT_COLOR, CLOCK_ICON, SKILLP_ID, DEFAULT_PFP, SKILLP_JOINED_UNIX_TIME



###time#related###############################################################################

def get_kst_time_stamp(source):
    if source == "/kst":
        format = "Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"
    else:
        format = "%Y/%m/%d %H:%M:%S %Z"

    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    kst_timestamp = now_korea.strftime(format)

    return kst_timestamp



def get_user_create_and_join_time(member):
    time1 = datetime.datetime.strptime(str(member.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    created_time = datetime.datetime.timestamp(time1)
    
    time2 = datetime.datetime.strptime(str(member.joined_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    joined_time = datetime.datetime.timestamp(time2)
    
    return int(created_time), int(joined_time)



def embed_get_server_create_time(interaction):
    time = datetime.datetime.strptime(str(interaction.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    created_time = datetime.datetime.timestamp(time)
    
    return int(created_time)


    
###user#attribute#getter###############################################################################

def get_nick_else_name(member):
    if member.nick != None:
        name = member.nick
    else:
        name = member.name

    return name



def get_user_avatar(member):
    if member.avatar is not None:
        member_avatar_url = member.avatar
    else:
        member_avatar_url = member.default_avatar

    return member_avatar_url


        
###info#related###############################################################################

from utilities.variables import SERVER_ID

def get_userinfo_embed(member):
    created_time, joined_time = get_user_create_and_join_time(member)
    name = get_nick_else_name(member)
    member_avatar_url = get_user_avatar(member)

    if member.id == SKILLP_ID and member.guild.id == SERVER_ID:
        join_time = f"<t:{SKILLP_JOINED_UNIX_TIME}>"
    else:
        join_time = f"<t:{joined_time}>"

    embed = embed_builder(title = f"User Information: `{name}`",
                          color = member.color,
                          thumbnail = member_avatar_url,

                          field_one_name = "ID",
                          field_one_value = member.id,
                          field_one_inline = False,
                                            
                          field_two_name = "Name:",
                          field_two_value = member,
                          field_two_inline = True,
                                            
                          field_three_name = "Top role",
                          field_three_value = member.top_role.mention,
                          field_three_inline = True,
                                            
                          field_four_name = "Status",
                          field_four_value = member.status,
                          field_four_inline = True,
                                            
                          field_five_name = "Created at:",
                          field_five_value = f"<t:{created_time}>",
                          field_five_inline = True,
                                            
                          field_six_name = "Joined at:",
                          field_six_value = join_time,
                          field_six_inline = True,

                          field_seven_name = "Boosted",
                          field_seven_value = bool(member.premium_since),
                          field_seven_inline = True)
    
    return embed



async def get_serverinfo_embed(client, interaction):
    created_time = embed_get_server_create_time(interaction)

    guild_with_counts = await client.fetch_guild(interaction.guild.id, with_counts=True)

    if interaction.guild.icon is not None:
        server_icon_url = interaction.guild.icon
    else:
        server_icon_url = DEFAULT_PFP

    embed = embed_builder(title = f"Server Information: `{interaction.guild.name}`",
                          color = BOT_COLOR,
                          thumbnail = server_icon_url,

                          field_one_name = "ID:",
                          field_one_value = interaction.guild.id,
                          field_one_inline = False,
                                            
                          field_two_name = "Owner:",
                          field_two_value = interaction.guild.owner.mention,
                          field_two_inline = True,
                                            
                          field_three_name = "Members:",
                          field_three_value = f"Total: {interaction.guild.member_count}\nOnline: {guild_with_counts.approximate_presence_count}",
                          field_three_inline = True,
                                            
                          field_four_name = "Channels:",
                          field_four_value = f"Text: {len(interaction.guild.text_channels)}\nVoice: {len(interaction.guild.voice_channels)}",
                          field_four_inline = True,
                                            
                          field_five_name = "Created at:",
                          field_five_value = f"<t:{created_time}>",
                          field_five_inline = True)

    return embed



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

    channel = await client.fetch_channel(id_list[1])
    message = await channel.fetch_message(id_list[2])

    return message, channel



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

###bulk#csv###############################################################################

import csv

def make_bulk_messages_csv(messages):
    messages.reverse()
    format = "%Y/%m/%d %H:%M:%S"

    with open('./storage/temp/bulk_messages.csv', 'w') as file:
        write = csv.writer(file)

        write.writerow(["Author ID", "Author Name", "Send at", "Content"])

    for i in range(len(messages)):
        with open('./storage/temp/bulk_messages.csv', 'a') as file:
            write = csv.writer(file)
            message_send_time = messages[i].created_at.strftime(format)
    
            write.writerow([f"{messages[i].author.id}", f"{messages[i].author.name}", f"{message_send_time}", f"{messages[i].content}"])

###embed#builder###############################################################################

from nextcord import Embed

def embed_builder(title = Embed.Empty,
                  title_url = Embed.Empty,
                  description = Embed.Empty,
                  color = Embed.Empty,
                  thumbnail = Embed.Empty,
                  image = Embed.Empty,
                  author = Embed.Empty,
                  author_url = Embed.Empty,
                  author_icon = Embed.Empty,
                  footer = Embed.Empty,
                  footer_icon = Embed.Empty,

                  field_one_name = Embed.Empty,
                  field_one_value = Embed.Empty,
                  field_one_inline = False,
                                    
                  field_two_name = Embed.Empty,
                  field_two_value = Embed.Empty,
                  field_two_inline = False,
                                    
                  field_three_name = Embed.Empty,
                  field_three_value = Embed.Empty,
                  field_three_inline = False,
                                    
                  field_four_name = Embed.Empty,
                  field_four_value = Embed.Empty,
                  field_four_inline = False,
                                    
                  field_five_name = Embed.Empty,
                  field_five_value = Embed.Empty,
                  field_five_inline = False,
                                    
                  field_six_name = Embed.Empty,
                  field_six_value = Embed.Empty,
                  field_six_inline = False,

                  field_seven_name = Embed.Empty,
                  field_seven_value = Embed.Empty,
                  field_seven_inline = False):
    embed = Embed(title = title,
                  url = title_url,
                  description = description,
                  color = color)

    embed.set_thumbnail(url = thumbnail)

    embed.set_image(url = image)

    if author != Embed.Empty:
        embed.set_author(name = author, url = author_url, icon_url = author_icon)

    if footer == Embed.Empty:
        format = "%Y/%m/%d %H:%M:%S %Z"
        now_utc = timedate.now(timezone('UTC'))
        now_korea = now_utc.astimezone(timezone('Asia/Seoul'))

        embed.set_footer(text = now_korea.strftime(format), icon_url = CLOCK_ICON)
    else:
        embed.set_footer(text = footer, icon_url = footer_icon)

    fields = [[field_one_name, field_one_value, field_one_inline],
              [field_two_name, field_two_value, field_two_inline],
              [field_three_name, field_three_value, field_three_inline],
              [field_four_name, field_four_value, field_four_inline],
              [field_five_name, field_five_value, field_five_inline],
              [field_six_name, field_six_value, field_six_inline],
              [field_seven_name, field_seven_value, field_seven_inline]]

    for i in range(len(fields)):
        if not "" == fields[i][0] and not None == fields[i][0] and not Embed.Empty == fields[i][0]:
            if not "" == fields[i][1] and not None == fields[i][1] and not Embed.Empty == fields[i][1]:
                embed.add_field(name = f"{fields[i][0]}"[:49], value = f"{fields[i][1]}"[:975], inline = fields[i][2])

    return embed