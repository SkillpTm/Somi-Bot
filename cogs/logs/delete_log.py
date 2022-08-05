###package#import###############################################################################

import nextcord
from nextcord import Color, Embed
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_forbidden_channels, checks_max_word_length
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import embed_kst_footer, embed_set_message_author, embed_attachments



class delete_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###delete#log###########################################################

    @commands.Cog.listener()
    async def on_message_delete(self,
                                message):
        interaction = message
        if not checks(interaction):
            return
        if not checks_forbidden_channels(interaction):
            return

        print(f"{message.author}: delete_log()\n{message.content}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        embed = Embed(description = f"{interaction.author.mention} deleted a message in: {message.channel.mention}",
                      colour=Color.red())
        embed_kst_footer(embed)
        embed_set_message_author(message, embed, title_name = "Message Deleted")
        checks_max_word_length(message, embed, source = "delete_log")

        target_channel = AUDIT_LOG
        await embed_attachments(target_channel, message, embed)

        uses_update("log_activations", "delete log")

def setup(client):
    client.add_cog(delete_log(client))