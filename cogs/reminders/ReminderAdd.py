###package#import###############################################################################

import nextcord
import random
import string
import time as unix_time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import create_reminder
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, time_to_seconds, embed_builder
from utilities.variables import BOT_COLOR



class ReminderAdd(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import reminder

    ###reminder#add###########################################################
    
    @reminder.subcommand(name = "add", description = "add a reminder to your reminder list")
    async def reminder_add(self,
                           interaction: nextcord.Interaction,
                           *,
                           time: str = nextcord.SlashOption(description="the time to be reminded in (input: xy | xw |xd | xh | xm | xs) Example: 5d7h28s)", required=True, min_length=2, max_length=30),
                           reminder: str = nextcord.SlashOption(description="what you want to be reminded about.", required=True, min_length=1, max_length=4096)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /reminder add {time}\n{reminder}")

        total_seconds = time_to_seconds(time)

        if total_seconds == 0:
            await interaction.response.send_message(f"`{time}` is not a valid time period. Make sure to use the formating in the input description.", ephemeral=True)
            return

        if total_seconds > 315576000: #10y in seconds
            await interaction.response.send_message(f"`{time}` is too long for a reminder. Reminders have to be under 10 years long.", ephemeral=True)
            return

        reminder_time = int(unix_time.time()) + int(total_seconds)
        delete_id = ""
        counter = 0
        while counter < 10:
            delete_id += string.digits[random.randint(0, 9)]
            counter += 1

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(description = reminder,
                              color = BOT_COLOR,
                              author = f"Reminder Set for {interaction.user}",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Time:",
                              field_one_value = f"<t:{reminder_time}:F>",
                              field_one_inline = False)

        await interaction.response.send_message(embed=embed)

        bot_reply = await interaction.original_message()

        create_reminder(interaction.user.id, reminder_time, bot_reply.jump_url, delete_id, reminder.replace("'", "‘"))

        uses_update("command_uses", "reminder add")



def setup(client):
    client.add_cog(ReminderAdd(client))