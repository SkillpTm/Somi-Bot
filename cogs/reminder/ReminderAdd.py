import random
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.managers import Config
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class ReminderAdd(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.reminder.subcommand(name="add", description="add a reminder to your reminder list")
    async def reminder_add(
        self,
        interaction: nextcord.Interaction,
        *,
        reminder_time: str = nextcord.SlashOption(
            name = "time",
            description = "the time to be reminded in (input: xy | xw |xd | xh | xm | xs) Example: 5d7h28s)",
            required = True,
            min_length = 2,
            max_length = 50
        ),
        reminder: str = nextcord.SlashOption(
            description = "what you want to be reminded about.",
            required = True,
            min_length = 1,
            max_length = 4096
        )
    ) -> None:
        """This command let's you add a reminder for anytime within the next 10 years"""

        if 0 == (total_seconds := Get.seconds_from_time(reminder_time)):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"`{reminder_time}` is not a valid time period. Make sure to use the formating in the input description."), ephemeral=True)
            return

        if total_seconds > 315576000: #10y in seconds
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"`{reminder_time}` is too long for a reminder. Reminders have to be under 10 years long."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        while True:
            reminder_id = random.randint(10**9, 10**10 - 1) # get a random 9 digit number

            # check if the reminder_id has already been used for this user
            if reminder_id not in [user_reminder[0] for user_reminder in await (await DBHandler(self.client.database, user_id=interaction.user.id).reminder()).get_list()]:
                break

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Reminder Set for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            description = reminder,
            fields = [
                [
                    "Time:",
                    f"<t:{int(time.time()) + total_seconds}:F>",
                    True
                ],

                [
                    "Reminder ID:",
                    f"`{reminder_id}`",
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed)

        bot_reply = await interaction.original_message()

        await (await DBHandler(self.client.database, user_id=interaction.user.id).reminder()).add(reminder_id, reminder_time, bot_reply.jump_url, reminder)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderAdd(client))