import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class DeleteLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def delete_log(self, message: nextcord.Message) -> None:
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

        self.client.Loggers.action_log(Get.log_message(
            message,
            "delete log",
            {"message": message.content}
        ))

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Message Deleted",
            author_icon = message.author.display_avatar.url,
            description = f"{message.author.mention} deleted a message in: {message.channel.mention}\n\n{message.content}",
            footer = "DEFAULT_KST_FOOTER"
        )

        embed, file_urls = EmbedFunctions.get_attachments(message.attachments, embed)
        sent_message = await message.guild.get_channel(audit_log_id).send(embed=embed)

        if file_urls:
            await sent_message.reply(content=file_urls, mention_author=False)

        CommandUsesDB("log_activations").update("delete log")



def setup(client: SomiBot) -> None:
    client.add_cog(DeleteLog(client))