import nextcord
import nextcord.ext.commands as nextcord_C
import os

from lib.db_modules import CommandUsesDB, ConfigDB
from lib.modules import Create, EmbedFunctions, Get
from lib.utilities import SomiBot



class PurgeLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def purge_log(self, messages: list[nextcord.Message]) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        audit_log_id: int = await ConfigDB(messages[0].guild.id, "AuditLogChannel").get_list(messages[0].guild)

        if not audit_log_id:
            return

        if messages[0].channel.id in await ConfigDB(messages[0].guild.id, "HiddenChannels").get_list(messages[0].guild):
            return

        # we only do this to get "entry" and with that data on who deleted the messages
        async for entry in messages[0].guild.audit_logs(limit=1, action=nextcord.AuditLogAction.message_bulk_delete):
            pass

        self.client.Loggers.action_log(Get().log_message(
            messages[0],
            "purge log",
            {"amount": str(len(messages))}
        ))

        # we create the csv first to reduce delay between the inital embed and the csv response message
        csv_name = Create().bulk_messages_csv(messages)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Purge Log:",
                    f"{entry.user.mention} purged: `{len(messages)} message(s)` in {entry.target.mention}",
                    False
                ]
            ]
        )

        sent_message = await messages[0].guild.get_channel(audit_log_id).send(embed=embed)
        await sent_message.reply(file=nextcord.File(csv_name), mention_author=False)
        os.remove(csv_name)

        CommandUsesDB("log_activations").update("purge log")



def setup(client: SomiBot) -> None:
    client.add_cog(PurgeLog(client))