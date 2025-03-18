import asyncio
import nextcord.ext.commands as nextcord_C
import requests

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class ReminderSend(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def infinite_reminder_loop(self) -> None:
        """infinite loop that will check every second all reminders, if they need to be send out and does so if they do"""

        while True:
            await self.reminder_send()
            await asyncio.sleep(1)

            # the following is to ensure that we don't get duplicates of this loop potentially sending the same reminder several times
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
        If the current time is larger or equal to the reminder time, then the reminder gets send to the user and deleted from the db.
        """  

        reminders_to_be_send = await (await DBHandler(self.client.PostgresDB).reminder()).get_upcoming() # the time comparison happens in here

        for reminder_to_be_send in reminders_to_be_send:
            reminder_id, user_id = reminder_to_be_send[0], reminder_to_be_send[1]

            _, reminder_link, reminder_text = await (await DBHandler(self.client.PostgresDB, user_id=user_id).reminder()).get_reminder(reminder_id)

            self.client.Loggers.action_log(f"reminder send ~ User: {user_id} ~ Guild: DM channel ~ args: [reminder: {reminder_text}]")

            embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                title = "Reminder Notification",
                title_url = reminder_link,
                description = reminder_text,
                footer = "DEFAULT_KST_FOOTER"
            )

            if user_id in Get.visible_users(self.client):
                user = await self.client.fetch_user(user_id)
                await user.send(embed=embed)
            else:
                self.client.Loggers.action_warning(f"reminder send: {user_id} couldn't be reminded, because their pms aren't open to the client")

            await (await DBHandler(self.client.PostgresDB, user_id=user_id).reminder()).delete(reminder_id)

            await (await DBHandler(self.client.PostgresDB).telemetry()).increment("reminder send")



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderSend(client))