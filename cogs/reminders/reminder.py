###package#import###############################################################################

import asyncio
import nextcord
from nextcord import Embed
from nextcord.ext import commands
import time as unix_time

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import delete_reminder, get_reminder_times, get_reminder_contents
from utilities.partial_commands import embed_kst_footer, embed_attachments, message_object_generation
from utilities.variables import BOT_COLOR



###reminder###########################################################

async def reminder_send(client):
    reminders = get_reminder_times()

    if not reminders == []:
        current_unix_time = int(unix_time.time())
        for reminder in reminders:
            time = reminder[1]
            if time <= current_unix_time:
                user_id = reminder[0]
                noti_user = await client.fetch_user(user_id)
                delete_id = reminder[2]

                bot_reply_link, clean_reminder = get_reminder_contents(user_id, delete_id)
                
                embed = Embed(title = "Reminder Notification",
                              url = bot_reply_link,
                              description = clean_reminder,
                              colour=BOT_COLOR)
                embed_kst_footer(embed)

                print(f"reminder() {noti_user}\n{clean_reminder}")

                message_object ,correct_channel = await message_object_generation(bot_reply_link, client)

                await embed_attachments(noti_user, message_object, embed)

                delete_reminder(user_id, delete_id)

                uses_update("command_uses", "reminder send")



class reminder(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###reminder#on#ready###########################################################

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await reminder_send(self.client)
            await asyncio.sleep(2)

def setup(client):
    client.add_cog(reminder(client))