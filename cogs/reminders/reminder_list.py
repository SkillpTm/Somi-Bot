###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import list_reminder
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_message_author
from utilities.variables import BOT_COLOR



class reminder_list(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import reminder

    ###reminder#list###########################################################

    @reminder.subcommand(name = "list", description = "A list of all your reminders")
    async def reminder_list(self,
                            interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /reminder list")

        amount, reminder_times, bot_reply_links, delete_ids = list_reminder(interaction.user.id)

        if amount == 0:
            await interaction.response.send_message("You don't have any reminders.", ephemeral=True)

            uses_update("command_uses", "reminder list")

            return

        i = 0

        embed = Embed(colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_message_author(interaction, embed, title_name = f"Reminder List for {interaction.user}")

        while i < amount and i < 9: #Field limit = 10
            embed.add_field(name = f"{i + 1}. Reminder:", value = f"<t:{reminder_times[i]}:F> // ID: {delete_ids[i]} - [Link]({bot_reply_links[i]})", inline = False)
            i += 1

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "reminder list")

def setup(client):
    client.add_cog(reminder_list(client))