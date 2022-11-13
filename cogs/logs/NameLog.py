###package#import###############################################################################

import nextcord
from nextcord import Color, Embed
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import get_user_avatar, embed_builder



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

        member_avatar_url = get_user_avatar(before)

        embed = embed_builder(title = f"{before} Changed Their {event}",
                              color = Color.yellow(),
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = f"{event} before:",
                              field_one_value = correct_before,
                              field_one_inline = False,

                              field_two_name = f"{event} after:",
                              field_two_value = correct_after,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("log_activations", "name log")

def setup(client):
    client.add_cog(name_log(client))