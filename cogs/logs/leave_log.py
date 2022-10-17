###package#import###############################################################################

import nextcord
from nextcord import Color
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.drop_user_data import drop_user_data_in_database
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import get_user_avatar, get_user_create_and_join_time, embed_builder



class leave_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###leave#log###########################################################

    @commands.Cog.listener()
    async def on_member_remove(self,
                               member):
        interaction = member
        if not checks(interaction):
            return

        print(f"leave_log() {member}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        member_avatar_url = get_user_avatar(member)
        created_time, joined_time = get_user_create_and_join_time(member)

        embed = embed_builder(title = f"Member Left: `{member}`",
                              color = Color.red(),
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "ID:",
                              field_one_value = member.id,
                              field_one_inline = False,

                              field_two_name = "Name:",
                              field_two_value = member.mention,
                              field_two_inline = True,
                              
                              field_three_name = "Created at:",
                              field_three_value = f"<t:{created_time}>",
                              field_three_inline = True,

                              field_four_name = "Joined at",
                              field_four_value = f"<t:{joined_time}>",
                              field_four_inline = True)

        await AUDIT_LOG.send(embed=embed)

        drop_user_data_in_database(member)

        uses_update("log_activations", "leave_log")

def setup(client):
    client.add_cog(leave_log(client))