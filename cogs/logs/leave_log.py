###package#import###############################################################################

import nextcord
from nextcord import Color, Embed
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import embed_kst_footer, embed_get_user_unix_time, embed_set_thumbnail



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
        
        embed = Embed(title = f"Member Left: `{member}`",
                      colour=Color.red())
        embed_kst_footer(embed)
        embed_set_thumbnail(member, embed)
        unix_time1, unix_time2 = embed_get_user_unix_time(member)

        fields = [("ID:", member.id, False),
                  ("Name:", member.mention, True),
                  ("Created at:", f"<t:{unix_time1}>", True),
                  ("Joined at", f"<t:{unix_time2}>", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await AUDIT_LOG.send(embed=embed)

        uses_update("log_activations", "leave_log")

def setup(client):
    client.add_cog(leave_log(client))