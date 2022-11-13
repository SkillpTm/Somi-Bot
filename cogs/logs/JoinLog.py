###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, SOMMUNGCHI_ID, WELCOME_CHANNEL_ID, WELCOME_GIF, SERVER_ID
from utilities.partial_commands import get_user_avatar, embed_builder



class JoinLog(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###welcome#message###########################################################
    
    @nextcord.ext.commands.Cog.listener()
    async def on_member_join(self,
                             member):
        if not checks(member.guild, member.user):
            return
        if member.guild.id != SERVER_ID:
            return

        print(f"join_log() {member}")

        DEFAULT_ROLE = nextcord.utils.get(member.guild.roles, id=SOMMUNGCHI_ID)
        WELCOME_CHANNEL = self.client.get_channel(WELCOME_CHANNEL_ID)

        await member.add_roles(DEFAULT_ROLE)
        await WELCOME_CHANNEL.send(f"Hey {member.mention}, welcome to Jeon Somi! What you waiting for - start chatting.\n{WELCOME_GIF}")

    ###join#log###########################################################

        created_time = int(time.mktime(member.created_at.timetuple()))
        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(member)

        embed = embed_builder(title = f"New Member Joined: `{member}`",
                              color = nextcord.Color.green(),
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
                              field_three_inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("log_activations", "join log")



def setup(client):
    client.add_cog(JoinLog(client))