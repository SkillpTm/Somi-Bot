###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, get_user_avatar, embed_builder
from utilities.variables import SKILLP_ID, SERVER_ID, SKILLP_JOINED_UNIX_TIME



class Userinfo(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###userinfo###########################################################

    @nextcord.slash_command(name = "ui", description = "gives information about a user", name_localizations = {country_tag:"userinfo" for country_tag in nextcord.Locale})
    async def userinfo(self,
                       interaction: nextcord.Interaction,
                       *,
                       member: nextcord.Member = nextcord.SlashOption(description="the user you want information about", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /userinfo {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        created_time = int(time.mktime(member.created_at.timetuple()))
        name = get_nick_else_name(member)
        member_avatar_url = get_user_avatar(member)

        if member.id == SKILLP_ID and member.guild.id == SERVER_ID:
            joined_time = SKILLP_JOINED_UNIX_TIME
        else:
            joined_time = int(time.mktime(member.joined_at.timetuple()))

        embed = embed_builder(title = f"User Information: `{name}`",
                              color = member.color,
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "ID:",
                              field_one_value = member.id,
                              field_one_inline = False,
                                                
                              field_two_name = "Name:",
                              field_two_value = member,
                              field_two_inline = True,
                                                
                              field_three_name = "Top role:",
                              field_three_value = member.top_role.mention,
                              field_three_inline = True,
                                                
                              field_four_name = "Status:",
                              field_four_value = member.status,
                              field_four_inline = True,
                                                
                              field_five_name = "Created at:",
                              field_five_value = f"<t:{created_time}>",
                              field_five_inline = True,
                                                
                              field_six_name = "Joined at:",
                              field_six_value = f"<t:{joined_time}>",
                              field_six_inline = True,

                              field_seven_name = "Boosted:",
                              field_seven_value = bool(member.premium_since),
                              field_seven_inline = True)

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "userinfo")



def setup(client):
    client.add_cog(Userinfo(client))