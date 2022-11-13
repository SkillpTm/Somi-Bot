###package#import###############################################################################

import asyncio
import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import delete_reminder, get_reminder_times, get_reminder_contents
from utilities.partial_commands import embed_attachments, message_object_generation, embed_builder
from utilities.variables import BOT_COLOR



###reminder###########################################################

async def reminder_send(client):
    reminders = get_reminder_times()

    if reminders == []:
        return

    current_unix_time = int(time.time())
    for reminder in reminders:
        reminder_time = reminder[1]

        if not reminder_time <= current_unix_time:
            continue

        user_id = reminder[0]
        noti_user = await client.fetch_user(user_id)
        delete_id = reminder[2]

        bot_reply_link, clean_reminder = get_reminder_contents(user_id, delete_id)

        print(f"reminder() {noti_user}\n{clean_reminder}")

        embed = embed_builder(title = "Reminder Notification",
                              title_url = bot_reply_link,
                              description = clean_reminder,
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER")

        message_object = await message_object_generation(bot_reply_link, client)

        await embed_attachments(noti_user, message_object, embed)

        delete_reminder(user_id, delete_id)

        uses_update("command_uses", "reminder send")



class ReminderSend(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###reminder#on#ready###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_ready(self):
        while True:
            await reminder_send(self.client)
            await asyncio.sleep(2)



def setup(client):
    client.add_cog(ReminderSend(client))