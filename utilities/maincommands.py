###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents)

###self#imports###############################################################################

from utilities.variables import SERVER_ID, MOD_CHANNELS



@client.slash_command(name='keyword', description='Gives notifications for selected keywords')
async def keyword(interaction: Interaction):
    pass



@client.slash_command(name='reminder', description='Add a reminder to be reminded about something')
async def reminder(interaction: Interaction):
    pass



@client.slash_command(name='custom', description='Make a custom command')
async def custom(interaction: Interaction):
    pass



###checks################################################################################

def checks(interaction):
    try:
        return interaction.guild.id == SERVER_ID and interaction.author.bot == False
    except:
        pass

    try:
        return interaction.guild.id == SERVER_ID and interaction.user.bot == False
    except:
        pass

    try:
        return interaction.guild.id == SERVER_ID and interaction.bot == False
    except:
        pass

    return False



def checks_forbidden_channels(interaction):
    return not interaction.channel.id in MOD_CHANNELS.values()



def checks_max_word_length(message, embed, source):
    if source != "reminder":
        message_content = message.content
    elif source == "reminder":
        message_content = message

    if message_content != "":
        if source == "delete_log":
            embed.add_field(name = "Deleted message:", value = message_content[:990], inline = True)
        elif source == "modmail":
            embed.add_field(name = "Message:", value = message_content[:990], inline = False)
        elif source == "edit_log before":
            embed.add_field(name = "Before:", value = message_content[:1000], inline = False)
        elif source == "edit_log after":
            embed.add_field(name = "After:", value = message_content[:1000], inline = False)

        if len(message_content) > 990:
            embed.add_field(name = "Part 2:", value = message_content[990:1980], inline = False)
        if len(message_content) > 1980:
            embed.add_field(name = "Part 3:", value = message_content[1980:2960], inline = False)
        if len(message_content) > 1980:
            embed.add_field(name = "Part 4:", value = message_content[1980:2960], inline = False)
        if len(message_content) > 2960:
            embed.add_field(name = "Part 5:", value = message_content[2960:3940], inline = False)
        if len(message_content) > 3940:
            embed.add_field(name = "Part 6:", value = message_content[3940:], inline = False)