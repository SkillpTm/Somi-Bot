####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import random
import time as unix_time

####################################################################################################

from lib.db_modules import ReminderDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class ReminderAdd(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import reminder

    ####################################################################################################
    
    @reminder.subcommand(name = "add", description = "add a reminder to your reminder list")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def reminder_add(
        self,
        interaction: nextcord.Interaction,
        *,
        time: str = nextcord.SlashOption(
            description="the time to be reminded in (input: xy | xw |xd | xh | xm | xs) Example: 5d7h28s)",
            required=True,
            min_length=2,
            max_length=50
        ),
        reminder: str = nextcord.SlashOption(
            description="what you want to be reminded about.",
            required=True,
            min_length=1,
            max_length=4096
        )
    ) -> None:
        """This command let's you add a reminder for anytime within the next 10 years"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/reminder add",
            {"time": time, "reminder": reminder}
        ))

        total_seconds = Get().seconds_from_time(time)

        if total_seconds == 0:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"`{time}` is not a valid time period. Make sure to use the formating in the input description."), ephemeral=True)
            return

        if total_seconds > 315576000: #10y in seconds
            await interaction.response.send_message(embed=EmbedFunctions().error(f"`{time}` is too long for a reminder. Reminders have to be under 10 years long."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        reminder_time = int(unix_time.time()) + total_seconds
        reminder_id: str = ""

        while not reminder_id:
            reminder_id = str(random.randint(10**9, 10**10 - 1))

            # check if the reminder_id has already been used for this user
            for reminder_element in ReminderDB(interaction.user.id).get_list():
                if reminder_id == str(reminder_element[2]):
                    reminder_id = ""
                    break

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"Reminder Set for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar,
            description = reminder,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Time:",
                    f"<t:{reminder_time}:F>",
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

        ReminderDB(interaction.user.id).add(reminder_time, bot_reply.jump_url, reminder_id, reminder)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderAdd(client))