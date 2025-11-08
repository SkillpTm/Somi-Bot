import asyncio
import nextcord.ext.commands as nextcord_C
import requests

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Config, Logger
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
                requests.get("https://www.google.com/", timeout=10)

            except (requests.ConnectionError, asyncio.CancelledError):
                self.client.restart()

    ####################################################################################################

    async def reminder_send(self) -> None:
        """
        This function pulls all reminder times from all users and compares them against the current time.
        If the current time is larger or equal to the reminder time, then the reminder gets send to the user and deleted from the db.
        """

        reminders = await (await DBHandler(self.client.database).reminder()).get_upcoming() 

        for reminder in reminders:
            reminder_id, user_id = reminder[0], reminder[1]

            _, reminder_link, reminder_text = await (await DBHandler(self.client.database, user_id=user_id).reminder()).get_reminder(reminder_id)

            Logger().action_log(
                self.client.get_user(user_id),
                "reminder send",
                {
                    "reminder id": str(reminder_id),
                    "reminder text": reminder_text
                }
            )

            embed = EmbedFunctions().builder(
                color = Config().BOT_COLOR,
                title = "Reminder Notification",
                title_url = reminder_link,
                description = reminder_text
            )

            if user_id in self.client.visible_users():
                user = await self.client.fetch_user(user_id)
                await user.send(embed=embed)
            else:
                Logger().action_warning(f"reminder send: {user_id} couldn't be reminded, because their pms aren't open to the client")

            await (await DBHandler(self.client.database, user_id=user_id).reminder()).delete(reminder_id)

            await (await DBHandler(self.client.database).telemetry()).increment("reminder send")



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderSend(client))