###package#import###############################################################################

import datetime
import humanfriendly
import nextcord
import pytz
import os
import sys

###self#imports###############################################################################

from utilities.variables import CLOCK_ICON, SKILLP_ID



###time#related###############################################################################

def get_kst_time_stamp(source):
    if source == "/kst":
        format = "Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"
    else:
        format = "%Y/%m/%d %H:%M:%S %Z"

    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    now_korea = now_utc.astimezone(pytz.timezone('Asia/Seoul'))
    kst_timestamp = now_korea.strftime(format)

    return kst_timestamp



###user#attribute#getter###############################################################################

def get_nick_else_name(member):
    name = None
    
    if hasattr(member, "name"):
        name = member.name

    if hasattr(member, "nick"):
        if member.nick != None:
            name = member.nick

    if name == None:
        name = "Deleted User"

    return name



def get_user_avatar(member):
    if member.avatar != None:
        member_avatar_url = member.avatar
    else:
        member_avatar_url = member.default_avatar

    return member_avatar_url



###attachment#related###############################################################################

async def embed_attachments(target_channel, message, embed, limit = None):
    if len(message.attachments) == 0:
        await target_channel.send(embed=embed)

    elif len(message.attachments) == 1 or limit == 1:
        if "image" in message.attachments[0].content_type:
            embed.set_image(url=message.attachments[0].url)

        await target_channel.send(embed=embed)

        if "image" not in message.attachments[0].content_type and limit == None:
            await target_channel.send(content = message.attachments[0].url)

    elif len(message.attachments) > 1:
        file_urls = ""

        for attachment in message.attachments:
            file_urls += f"{attachment.url}\n"

        await target_channel.send(embed=embed)
        await target_channel.send(content=file_urls)



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

    clean_time = time.replace(" ", "").lower()
    parse_data = ["s", "m", "h", "d", "w", "y"]
    position_in_string = [clean_time.find("s"), clean_time.find("m"), clean_time.find("h"), clean_time.find("d"), clean_time.find("w"), clean_time.find("y")]

    for index, position in enumerate(position_in_string):
        if position > 0:
            for i in range(len(clean_time[:position])):
                if not clean_time[position -i -1].isdigit():
                    break
                parse_data[index] = "".join((clean_time[position -i -1], parse_data[index]))

    for data in parse_data:
        if len(data) > 1:
            total_seconds += int(humanfriendly.parse_timespan(data))

            if data.endswith("y"): #in Humanfriendly a year is only 364 days
                total_seconds += int(humanfriendly.parse_timespan(f"{data[:-1]}d"))

    return total_seconds



###message#object#related###############################################################################

async def message_object_generation(link, client):
    ids_list = link.split("/")

    channel = await client.fetch_channel(ids_list[5])
    message = await channel.fetch_message(ids_list[6])

    return message



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



###bulk#csv###############################################################################

import csv

def make_bulk_messages_csv(messages):
    messages.reverse()
    write = csv.writer(file)

    with open('./storage/temp/bulk_messages.csv', 'w') as file:
        write.writerow(["Author ID", "Author Name", "Send at", "Content"])

    for message in messages:
        with open('./storage/temp/bulk_messages.csv', 'a') as file:
            message_send_time = message.created_at.strftime("%Y/%m/%d %H:%M:%S")
    
            write.writerow([f"{message.author.id}", f"{message.author.name}", f"{message_send_time}", f"{message.content}"])



###embed#builder###############################################################################

def embed_builder(title = None,
                  title_url = None,
                  description = None,
                  color = None,
                  thumbnail = None,
                  image = None,
                  author = None,
                  author_url = None,
                  author_icon = None,
                  footer = None,
                  footer_icon = None,

                  field_one_name = None,
                  field_one_value = None,
                  field_one_inline = False,
                                    
                  field_two_name = None,
                  field_two_value = None,
                  field_two_inline = False,
                                    
                  field_three_name = None,
                  field_three_value = None,
                  field_three_inline = False,
                                    
                  field_four_name = None,
                  field_four_value = None,
                  field_four_inline = False,
                                    
                  field_five_name = None,
                  field_five_value = None,
                  field_five_inline = False,
                                    
                  field_six_name = None,
                  field_six_value = None,
                  field_six_inline = False,

                  field_seven_name = None,
                  field_seven_value = None,
                  field_seven_inline = False):
    embed = nextcord.Embed(title = title,
                           url = title_url,
                           description = description,
                           color = color)

    embed.set_thumbnail(url = thumbnail)

    embed.set_image(url = image)

    if author != None:
        embed.set_author(name = author, url = author_url, icon_url = author_icon)

    if footer == "DEFAULT_KST_FOOTER":
        now_utc = datetime.datetime.now(pytz.timezone('UTC'))
        now_korea = now_utc.astimezone(pytz.timezone('Asia/Seoul'))

        embed.set_footer(text = now_korea.strftime("%Y/%m/%d %H:%M:%S %Z"), icon_url = CLOCK_ICON)
    elif footer != None:
        embed.set_footer(text = footer, icon_url = footer_icon)

    fields = [[field_one_name, field_one_value, field_one_inline],
              [field_two_name, field_two_value, field_two_inline],
              [field_three_name, field_three_value, field_three_inline],
              [field_four_name, field_four_value, field_four_inline],
              [field_five_name, field_five_value, field_five_inline],
              [field_six_name, field_six_value, field_six_inline],
              [field_seven_name, field_seven_value, field_seven_inline]]

    for field in fields:
        if field[0] == "" or field[0] == None:
            break

        if field[1] == "" or field[1] == None:
            break
        
        embed.add_field(name = f"{field[0]}"[:49], value = f"{field[1]}"[:975], inline = field[2])

    return embed



###autocomplete#releated###############################################################################

def string_search_to_list(string, list):
    if string == "":
        string_list = [str(list_object) for list_object in list]
        return string_list

    get_near_objects = [str(list_object) for list_object in list if str(list_object).lower().startswith(string.lower())]

    if get_near_objects == []:
        get_near_objects = [str(list_object) for list_object in list if string.lower() in str(list_object).lower()]

    return get_near_objects



###view#releated###############################################################################

async def deactivate_view_children(self):
    for child in self.children:
        child.disabled = True
    if hasattr(self, "response"):
        await self.response.edit(view=self)
    elif hasattr(self, "interaction"):
        await self.interaction.edit_original_message(view=self)



###level#roles###############################################################################

from database.database_levelroles import get_server_level_roles
from database.database_levels import get_all_user_levels

async def level_roles_apply(server: nextcord.guild, input_users: list[list[tuple[int, int]]] = [[0, 0]]) -> None:
    levelroles = get_server_level_roles(server.id)
    if input_users == [[0, 0]]:
        input_users = get_all_user_levels(server.id)

    if levelroles == []:
        return

    server_level_roles = []
    users_and_level_roles = {}

    for levelrole in levelroles:
        server_level_roles.append(server.get_role(int(levelrole[0])))

    for levelrole in levelroles:
        for user in input_users:
            if user[1] >= levelrole[1]:
                users_and_level_roles.update({user[0]: int(levelrole[0])})

    for user_id, levelrole_id in users_and_level_roles.items():
        member = server.get_member(user_id)
        role = server.get_role(levelrole_id)

        if not role in member.roles:
            for server_level_role in server_level_roles:
                if server_level_role in member.roles:
                    await member.remove_roles(server_level_role)

            await member.add_roles(role)



async def remove_level_roles_from_members(server: nextcord.guild, role: nextcord.Role) -> None:
    all_users = get_all_user_levels(server.id)

    for user in all_users:
        member = server.get_member(user[0])

        if role in member.roles:
            await member.remove_roles(role)

    await level_roles_apply(server)