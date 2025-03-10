import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import os

from lib.dbModules import DBHandler
from lib.modules import Create, EmbedFunctions, Get
from lib.utilities import SomiBot



class PurgeLog(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def purge_log(self, messages: list[nextcord.Message]) -> None:
        """A log that activates, when someone gets purged without using the bot"""

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=messages[0].guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        if messages[0].channel.id in await (await DBHandler(self.client.PostgresDB, server_id=messages[0].guild.id).hidden_channel()).get_list():
            return

        # we only do this to get "entry" and with that data on who deleted the messages
        async for entry in messages[0].guild.audit_logs(limit=1, action=nextcord.AuditLogAction.message_bulk_delete):
            if (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds() < 5:
                return

        self.client.Loggers.action_log(Get.log_message(
            messages[0],
            "purge log",
            {"amount": str(len(messages))}
        ))

        # we create the csv first to reduce delay between the inital embed and the csv response message
        csv_name = Create.bulk_messages_csv(messages)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = "Mod Activity",
            author_icon = entry.user.display_avatar.url,
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

        await (await DBHandler(self.client.PostgresDB).telemetry()).increment("purge log")



def setup(client: SomiBot) -> None:
    client.add_cog(PurgeLog(client))