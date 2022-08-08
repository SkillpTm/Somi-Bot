###package#import###############################################################################

import nextcord
from nextcord import Color
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, SOMMUNGCHI_ID, WELCOME_CHANNEL_ID, WELCOME_GIF
from utilities.partial_commands import get_user_avatar, get_user_create_and_join_time, embed_builder



class join_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###welcome#message###########################################################
    
    @commands.Cog.listener()
    async def on_member_join(self,
                             member):
        if not checks(member):
            return

        print(f"join_log() {member}")

        DEFAULT_ROLE = nextcord.utils.get(member.guild.roles, id=SOMMUNGCHI_ID)
        WELCOME_CHANNEL = self.client.get_channel(WELCOME_CHANNEL_ID)

        await member.add_roles(DEFAULT_ROLE)
        await WELCOME_CHANNEL.send(f"Hey {member.mention}, welcome to Jeon Somi! What you waiting for - start chatting. \n{WELCOME_GIF}")

    ###join#log###########################################################

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(member)
        created_time, joined_time = get_user_create_and_join_time(member)

        embed = embed_builder(title = f"New Member Joined: `{member}`",
                              color = Color.green(),
                              thumbnail = member_avatar_url,

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
    client.add_cog(join_log(client))