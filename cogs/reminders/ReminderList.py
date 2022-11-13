###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import list_reminder
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import BOT_COLOR



class ReminderList(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import reminder

    ###reminder#list###########################################################

    @reminder.subcommand(name = "list", description = "a list of all your reminders")
    async def reminder_list(self,
                            interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /reminder list")

        reminder_times, bot_reply_links, delete_ids, clean_reminders = list_reminder(interaction.user.id)

        if len(clean_reminders) == 0:
            await interaction.response.send_message("You don't have any reminders.", ephemeral=True)

            uses_update("command_uses", "reminder list")

            return

        output = ""
        i = 0

        #TODO add pages to this
        while i < len(clean_reminders):
            if len(clean_reminders[i]) > 30:
                output += f"<t:{reminder_times[i]}:F> // ID: {delete_ids[i]} - [Link]({bot_reply_links[i]})\nReminder: `{clean_reminders[i][:30]}...`\n\n"
            else:
                output += f"<t:{reminder_times[i]}:F> // ID: {delete_ids[i]} - [Link]({bot_reply_links[i]})\nReminder: `{clean_reminders[i][:30]}`\n\n"
            i += 1

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(description = output[:4096],
                              color = BOT_COLOR,
                              author = f"Reminder List for {interaction.user}",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER")

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "reminder list")



def setup(client):
    client.add_cog(ReminderList(client))