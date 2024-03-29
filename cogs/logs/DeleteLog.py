####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C

####################################################################################################

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class DeleteLog(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_message_delete(self,
                                message: nextcord.Message):
        """This function will create a delete-log message, if a guild has an audit-log-channel and if the message wasn't in a hidden-channel."""

        if not Checks.message_in_guild(self.client, message):
            return

        if not message.content and len(message.attachments) < 1:
            return

        audit_log_id: int = await ConfigDB(message.guild.id, "AuditLogChannel").get_list(message.guild)

        if not audit_log_id:
            return

        if message.channel.id in await ConfigDB(message.guild.id, "HiddenChannels").get_list(message.guild):
            return

        self.client.Loggers.action_log(f"Guild: {message.guild.id} ~ Channel: {message.channel.id} ~ User: {message.author.id} ~ delete_log()\nMessage: {message.content}")

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            author = "Message Deleted",
            author_icon = message.author.display_avatar,
            description = f"{message.author.mention} deleted a message in: {message.channel.mention}\n\n{message.content}"[:4095],
            footer = "DEFAULT_KST_FOOTER"
        )

        embed, file_urls = EmbedFunctions().get_attachments(message.attachments, embed)
        audit_log_channel = message.guild.get_channel(audit_log_id)

        sent_message = await audit_log_channel.send(embed=embed)

        if file_urls != "":
            await sent_message.reply(content=file_urls, mention_author=False)

        CommandUsesDB("log_activations").update("delete log")



def setup(client: SomiBot):
    client.add_cog(DeleteLog(client))