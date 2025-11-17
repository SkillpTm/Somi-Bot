import asyncio
import time

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Config, Logger
from lib.modules import SomiBot



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

        async for entry in db.Reminder._.get_multiple(order_by=db.Reminder.TIME, order=Order.ASCENDING):
            if db.Reminder.TIME.retrieve(entry) > int(time.time()):
                return

            Logger().action_log(
                self.client.get_user(db.Reminder.USER.retrieve(entry)),
                "reminder send",
                {
                    "reminder id": str(db.Reminder.ID.retrieve(entry)),
                    "reminder text": db.Reminder.MESSAGE.retrieve(entry)
                }
            )

            embed = EmbedFunctions().builder(
                color = Config().BOT_COLOR,
                title = "Reminder Notification",
                title_url = db.Reminder.LINK.retrieve(entry),
                description = db.Reminder.MESSAGE.retrieve(entry)
            )

            try:
                user = await self.client.fetch_user(db.Reminder.USER.retrieve(entry))
                await user.send(embed=embed)
            except (nextcord.NotFound, nextcord.Forbidden):
                Logger().action_warning(f"reminder send: {db.Reminder.USER.retrieve(entry)} couldn't be reminded, because their pms aren't open to the client")

            await db.Reminder._.delete(db.Reminder.ID.retrieve(entry))
            await db.Telemetry.AMOUNT.increment("reminder send")



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderSend(client))