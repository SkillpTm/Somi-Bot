###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.drop_user_data import drop_user_data_in_database
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, SERVER_ID
from utilities.partial_commands import get_user_avatar, embed_builder



class LeaveLog(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###leave#log###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_member_remove(self,
                               member):
        if not checks(member.guild, member.user):
            return
        if member.guild.id != SERVER_ID:
            return

        print(f"leave_log() {member}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        joined_time = int(time.mktime(member.joined_at.timetuple()))
        created_time = int(time.mktime(member.created_at.timetuple()))
        member_avatar_url = get_user_avatar(member)

        embed = embed_builder(title = f"Member Left: `{member}`",
                              color = nextcord.Color.red(),
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
    client.add_cog(LeaveLog(client))