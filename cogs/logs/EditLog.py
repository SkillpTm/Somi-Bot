import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class EditLog(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_message_edit(self,
                              message_before: nextcord.Message,
                              message_after: nextcord.Message):
        """This function will create an edit-log message, if a guild has an audit-log-channel and if the message wasn't in a hidden-channel."""

        if not Checks.message_in_guild(self.client, message_before):
            return

        audit_log_id: int = await ConfigDB(message_before.guild.id, "AuditLogChannel").get_list(message_before.guild)

        if not audit_log_id:
            return

        if message_before.channel.id in await ConfigDB(message_before.guild.id, "HiddenChannels").get_list(message_before.guild):
            return

        if message_before.content == message_after.content:
            return

        self.client.Loggers.action_log(f"Guild: {message_before.guild.id} ~ Channel: {message_before.channel.id} ~ User: {message_before.author.id} ~ edit_log()\nMessage before: {message_before.content}\nMessage after: {message_after.content}")


        if len(message_before.content) < 1024 and len(message_after.content) < 1024:
            embed = EmbedFunctions().builder(
                color = nextcord.Color.yellow(),
                author = "Message Edited",
                author_icon = message_before.author.display_avatar,
                description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})",
                footer = "DEFAULT_KST_FOOTER",
                fields = [
                    [
                        "Before:",
                        message_before.content[:1023],
                        False
                    ],

                    [
                        "After:",
                        message_after.content[:1023],
                        False
                    ]
                ]
            )

            embed, file_urls = EmbedFunctions().get_attachments(message_before.attachments, embed)
            audit_log_channel = message_before.guild.get_channel(audit_log_id)

            sent_message = await audit_log_channel.send(embed=embed)

            if file_urls != "":
                await sent_message.reply(content=file_urls, mention_author=False)

            CommandUsesDB("log_activations").update("edit log")
            return


        embed_before = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Message Edited",
            author_icon = message_before.author.display_avatar,
            description = f"{message_before.author.mention} edited a message in: {message_before.channel.mention} - [Link]({message_before.jump_url})\n**Before:**\n{message_before.content}"[:4095]
        )

        embed_after = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            description = f"**After:**\n{message_after.content}"[:4095],
            footer = "DEFAULT_KST_FOOTER"
        )

        embed_after, file_urls = EmbedFunctions().get_attachments(message_before.attachments, embed_after)
        audit_log_channel = message_before.guild.get_channel(audit_log_id)

        await audit_log_channel.send(embed=embed_before)
        sent_message = await audit_log_channel.send(embed=embed_after)

        if file_urls != "":
            await sent_message.reply(content=file_urls, mention_author=False)

        CommandUsesDB("log_activations").update("edit log")



def setup(client: SomiBot):
    client.add_cog(EditLog(client))