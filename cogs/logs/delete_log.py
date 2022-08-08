###package#import###############################################################################

import nextcord
from nextcord import Color
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_forbidden_channels, checks_max_word_length
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import get_user_avatar, embed_attachments, embed_builder



class delete_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###delete#log###########################################################

    @commands.Cog.listener()
    async def on_message_delete(self,
                                message):
        if not checks(message):
            return
        if not checks_forbidden_channels(message):
            return

        print(f"{message.author}: delete_log()\n{message.content}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(message.author)

        embed = embed_builder(description = f"{message.author.mention} deleted a message in: {message.channel.mention}",
                              color = Color.red(),
                              author = "Message Deleted",
                              author_icon = member_avatar_url)

        checks_max_word_length(message, embed, source = "delete_log")

        await embed_attachments(AUDIT_LOG, message, embed)

        uses_update("log_activations", "delete log")

def setup(client):
    client.add_cog(delete_log(client))