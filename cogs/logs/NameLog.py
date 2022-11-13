###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, SERVER_ID
from utilities.partial_commands import get_user_avatar, embed_builder



class NameLog(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###name#log###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_member_update(self,
                               before,
                               after):
        if not checks(before.guild, before.user):
            return

        if before.guild.id != SERVER_ID:
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
                              color = nextcord.Color.yellow(),
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
    client.add_cog(NameLog(client))