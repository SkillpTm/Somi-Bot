####################################################################################################

import asyncio
import nextcord.ext.commands as nextcord_C

####################################################################################################

from lib.db_modules import CommandUsesDB, ReminderDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class ReminderSend(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    async def infinite_reminder_loop(self):
        while True:
            await self.reminder_send()
            await asyncio.sleep(2)

    ####################################################################################################

    async def reminder_send(self) -> None:
        """
        This function pulls all reminder times from all users and compares them against the current time.
        If the current time is larger or egal to the reminder time, then the reminder gets send to the user and delete from the db.
        """  

        reminders = ReminderDB().get_times()

        if reminders == []:
            return

        for reminder in reminders:
            user_id = reminder[0]
            noti_user = await self.client.fetch_user(user_id)
            delete_id = reminder[2]

            bot_reply_link, reminder_text = ReminderDB().get_contents(user_id, delete_id)

            self.client.Loggers.action_log(f"User: {user_id} ~ reminder()\n{reminder_text}")

            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = "Reminder Notification",
                title_url = bot_reply_link,
                description = reminder_text,
                footer = "DEFAULT_KST_FOOTER"
            )

            try:
                await noti_user.send(embed=embed)
            except:
                self.client.Loggers.action_warning(f"reminder() {noti_user.id} couldn't be reminded, because their pms aren't open to the client")

            ReminderDB().delete(user_id, delete_id)

            CommandUsesDB().uses_update("command_uses", "reminder send")



def setup(client: SomiBot):
    client.add_cog(ReminderSend(client))