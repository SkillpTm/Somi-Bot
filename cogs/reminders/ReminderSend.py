####################################################################################################

import asyncio
import nextcord.ext.commands as nextcord_C
import requests

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
            await asyncio.sleep(1)

            try:
                if self.client.is_closed() and not self.client.is_ready():
                    break
                requests.get("https://www.google.com/")

            except (requests.ConnectionError, asyncio.CancelledError):
                self.client.restart()

    ####################################################################################################

    async def reminder_send(self) -> None:
        """
        This function pulls all reminder times from all users and compares them against the current time.
        If the current time is larger or egal to the reminder time, then the reminder gets send to the user and delete from the db.
        """  

        reminders = ReminderDB(self.client.user.id).get_current()

        for reminder in reminders:

            reminder_time, reminder_link, reminder_id, reminder_text = ReminderDB(reminder[0]).get_reminder(reminder[1])

            self.client.Loggers.action_log(f"User: {reminder[0]} ~ reminder()\n{reminder_text}")

            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = "Reminder Notification",
                title_url = reminder_link,
                description = reminder_text,
                footer = "DEFAULT_KST_FOOTER"
            )

            try:
                reminder_user = await self.client.fetch_user(reminder[0])
                await reminder_user.send(embed=embed)
            except:
                self.client.Loggers.action_warning(f"reminder() {reminder[0]} couldn't be reminded, because their pms aren't open to the client")

            ReminderDB(reminder[0]).delete(reminder_id)

            CommandUsesDB("command_uses").update("reminder send")



def setup(client: SomiBot):
    client.add_cog(ReminderSend(client))