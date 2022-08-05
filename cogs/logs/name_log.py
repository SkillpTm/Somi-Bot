###package#import###############################################################################

import nextcord
from nextcord import Color, Embed
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import embed_kst_footer, embed_set_thumbnail



class name_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###name#log###########################################################

    @commands.Cog.listener()
    async def on_member_update(self,
                               before,
                               after):
        if not checks(before):
            return

        if before == after and before.nick == after.nick:
            return

        print(f"name_log()\nName: {before} --> {after}\nNickname: {before.nick} --> {after.nick}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        if before.nick != after.nick:
            correct_before = before.nick
            correct_after = after.nick
            event = "Nickname"
        elif before != after:
            correct_before = before
            correct_after = after
            event = "Name ID"
            
        embed = Embed(title=f"{before} Changed Their {event}",
                      colour=Color.yellow())
        embed_kst_footer(embed)
        embed_set_thumbnail(before, embed)
        embed.add_field(name = f"{event} before:", value = correct_before, inline = False)
        embed.add_field(name = f"{event} after", value = correct_after, inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("log_activations", "name log")

def setup(client):
    client.add_cog(name_log(client))