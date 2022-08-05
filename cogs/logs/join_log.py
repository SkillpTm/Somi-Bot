###package#import###############################################################################

import nextcord
from nextcord import Color, Embed
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, SOMMUNGCHI_ID, WELCOME_CHANNEL_ID, WELCOME_GIF
from utilities.partial_commands import embed_kst_footer, embed_get_member_join_unix_time, embed_set_thumbnail



class join_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###welcome#message###########################################################
    
    @commands.Cog.listener()
    async def on_member_join(self,
                             member):
        interaction = member
        if not checks(interaction):
            return

        print(f"join_log() {member}")

        DEFAULT_ROLE = nextcord.utils.get(member.guild.roles, id=SOMMUNGCHI_ID)
        WELCOME_CHANNEL = self.client.get_channel(WELCOME_CHANNEL_ID)

        await member.add_roles(DEFAULT_ROLE)
        await WELCOME_CHANNEL.send(f"Hey {member.mention}, welcome to Jeon Somi! What you waiting for - start chatting. \n{WELCOME_GIF}")

    ###join#log###########################################################

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        embed = Embed(title = f"New Member Joined: `{member}`",
                      colour=Color.green())
        embed_kst_footer(embed)
        embed_set_thumbnail(member, embed)
        unix_time = embed_get_member_join_unix_time(member)
        
        fields = [("ID:", member.id, False),
                  ("Name:", member.mention, True),
                  ("Created at:", f"<t:{unix_time}>", True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await AUDIT_LOG.send(embed=embed)

        uses_update("log_activations", "join log")

def setup(client):
    client.add_cog(join_log(client))