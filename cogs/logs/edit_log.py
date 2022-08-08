###package#import###############################################################################

import nextcord
from nextcord import Color
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_forbidden_channels, checks_max_word_length
from utilities.variables import AUDIT_LOG_ID
from utilities.partial_commands import embed_attachments, get_user_avatar, embed_builder



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
            member_avatar_url = get_user_avatar(message_before.author)

            embed = embed_builder(despcription = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                                  color = Color.yellow(),
                                  author = "Message Edited",
                                  author_icon = member_avatar_url,

                                  field_one_name = "Before:",
                                  field_one_value = message_before.content[:1000],
                                  field_one_inline = False,

                                  field_two_name = "After:",
                                  field_two_value = message_after.content[:1000],
                                  field_two_inline = False)

            await embed_attachments(target_channel = AUDIT_LOG, message = message_before, embed = embed)

        else:
            member_avatar_url = get_user_avatar(message_before.author)

            embed_before = embed_builder(despcription = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                                         color = Color.yellow(),
                                         author = "Message Edited: Before",
                                         author_icon = member_avatar_url)

            embed_after = embed_builder(despcription = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                                        color = Color.yellow(),
                                        author = "Message Edited: After",
                                        author_icon = member_avatar_url)

            checks_max_word_length(message_before, embed_before, source = "edit_log before")
            checks_max_word_length(message_after, embed_after, source = "edit_log after")

            await AUDIT_LOG.send(embed=embed_before)
            await embed_attachments(target_channel = AUDIT_LOG, message = message_after, embed = embed_after)


        uses_update("log_activations", "edit log")

def setup(client):
    client.add_cog(edit_log(client))