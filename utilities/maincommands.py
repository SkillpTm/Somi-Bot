###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from utilities.variables import SERVER_ID, MOD_CATEGORY_ID



@client.slash_command(name='keyword', description='gives notifications for selected keywords')
async def keyword(self, interaction: nextcord.Interaction):
    pass



@client.slash_command(name='reminder', description='add a reminder to be reminded about something')
async def reminder(self, interaction: nextcord.Interaction):
    pass



@client.slash_command(name='custom', description='make a custom command')
async def custom(self, interaction: nextcord.Interaction):
    pass



@client.slash_command(name='lf', description='a LastFm releated command')
async def lastfm(self, interaction: nextcord.Interaction):
    pass



###checks################################################################################

def checks(guild, user):
    return guild.id == SERVER_ID and user.bot == False



def checks_forbidden_channels(channel):
    if not hasattr(channel, "category"):
        return True
    return not channel.category.id == MOD_CATEGORY_ID



def checks_max_word_length(message, embed, source):
    FIELD_NAMES = {"delete_log": "Deleted message:", "edit_log before": "Before:", "edit_log after": "After:"}

    if message.content != "":
        embed.add_field(name = FIELD_NAMES[source], value = message.content[:990], inline = True)

        if len(message.content) > 990:
            embed.add_field(name = "Part 2:", value = message.content[990:1980], inline = False)
        if len(message.content) > 1980:
            embed.add_field(name = "Part 3:", value = message.content[1980:2960], inline = False)
        if len(message.content) > 2960:
            embed.add_field(name = "Part 4:", value = message.content[2960:3940], inline = False)
        if len(message.content) > 3940:
            embed.add_field(name = "Part 5:", value = message.content[3940:], inline = False)