import datetime
import random
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class ReminderAdd(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.reminder.subcommand(Commands().data["reminder add"].name, Commands().data["reminder add"].description)
    async def reminder_add(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        reminder_time: str = nextcord.SlashOption(
            Commands().data["reminder add"].parameters["reminder_time"].name,
            Commands().data["reminder add"].parameters["reminder_time"].description,
            required = True,
            min_length = 2,
            max_length = 50
        ),
        reminder: str = nextcord.SlashOption(
            Commands().data["reminder add"].parameters["reminder"].name,
            Commands().data["reminder add"].parameters["reminder"].description,
            required = True,
            min_length = 1,
            max_length = 4096
        )
    ) -> None:
        """This command let's you add a reminder for anytime within the next 10 years"""

        if 0 == (total_seconds := Get.seconds_from_time(reminder_time)):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"`{reminder_time}` is not a valid time period. Make sure to use the formating in the input description."), ephemeral=True)
            return

        if total_seconds > 315576000: #10y in seconds
            await interaction.send(embed=EmbedFunctions.get_error_message(f"`{reminder_time}` is too long for a reminder. Reminders have to be under 10 years long."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        reminder_timestamp = int(time.time()) + total_seconds

        while True:
            reminder_id = random.randint(10**8, 10**9 - 1) # get a random 9 digit number

            # check if the reminder_id has already been used for this user
            if not await db.Reminder.ID.get(reminder_id):
                break

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            author = f"Reminder Set for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            description = reminder,
            footer = "You'll be reminded:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = datetime.datetime.fromtimestamp(reminder_timestamp),
            fields = [
                EmbedField(
                    "Reminder ID:",
                    f"`{reminder_id}`",
                    True
                )
            ]
        )

        await interaction.send(embed=embed)

        bot_reply = await interaction.original_message()

        await db.Reminder._.add({
            db.Reminder.ID: reminder_id,
            db.Reminder.USER: interaction.user.id,
            db.Reminder.TIME: reminder_timestamp,
            db.Reminder.LINK: bot_reply.jump_url,
            db.Reminder.MESSAGE: reminder
        })



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderAdd(client))