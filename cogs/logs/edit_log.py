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



class edit_log(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###edit#log###########################################################

    @commands.Cog.listener()
    async def on_message_edit(self,
                              message_before,
                              message_after):
        if not checks(interaction = message_before):
            return
        if not checks_forbidden_channels(interaction = message_before):
            return

        if message_before.content == message_after.content:
            return

        print(f"{message_before.author}: edit_log()\nbefore: {message_before.content}\n\nafter: {message_after.content}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        if len(message_before.content) < 1000 and len(message_after.content) < 1000:

            embed = Embed(description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                            colour=Color.yellow())
            embed_kst_footer(embed)
            embed_set_message_author(message_before, embed, title_name = "Message Edited")

            if message_before.content == "":
                before_content = "`No content`"
            else:
                before_content = message_before.content

            if message_after.content == "":
                after_content = "`No content`"
            else:
                after_content = message_after.content

            embed.add_field(name = "Before:", value = before_content[:1000], inline = False)
            embed.add_field(name = "After:", value = after_content[:1000], inline = False)

            await embed_attachments(target_channel = AUDIT_LOG, message = message_before, embed = embed)

        else:
            embed_before = Embed(description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                            colour=Color.yellow())
            embed_after = Embed(description = f"{message_after.author.mention} edited a message in: {message_after.channel.mention} - [Link]({message_after.jump_url})",
                            colour=Color.yellow())

            embed_kst_footer(embed = embed_before)
            embed_kst_footer(embed = embed_after)

            embed_set_message_author(message = message_before, embed = embed_before, title_name = "Message Edited: Before")
            embed_set_message_author(message = message_after, embed = embed_after, title_name = "Message Edited: After")

            if message_before.content == "":
                before_content = "`No content`"
            else:
                before_content = message_before.content

            if message_after.content == "":
                after_content = "`No content`"
            else:
                after_content = message_after.content

            checks_max_word_length(message = message_before, embed = embed_before, source = "edit_log before")
            checks_max_word_length(message = message_after, embed = embed_after, source = "edit_log after")

            await AUDIT_LOG.send(embed=embed_before)
            await embed_attachments(target_channel = AUDIT_LOG, message = message_after, embed = embed_after)


        uses_update("log_activations", "edit log")

def setup(client):
    client.add_cog(edit_log(client))