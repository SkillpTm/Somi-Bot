###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_forbidden_channels, checks_max_word_length
from utilities.variables import AUDIT_LOG_ID,SERVER_ID
from utilities.partial_commands import get_user_avatar, embed_attachments, embed_builder



class DeleteLog(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###delete#log###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_message_delete(self,
                                message):
        if not checks(message.guild, message.author):
            return
        if message.guild.id != SERVER_ID or not checks_forbidden_channels(message.channel):
            return

        print(f"{message.author}: delete_log()\n{message.content}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(message.author)

        embed = embed_builder(description = f"{message.author.mention} deleted a message in: {message.channel.mention}",
                              color = nextcord.Color.red(),
                              author = "Message Deleted",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER")

        checks_max_word_length(message, embed, source = "delete_log")

        await embed_attachments(AUDIT_LOG, message, embed)

        uses_update("log_activations", "delete log")



def setup(client):
    client.add_cog(DeleteLog(client))