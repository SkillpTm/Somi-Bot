###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import delete_reminder, delete_all_user_reminders
from utilities.maincommands import checks



class question_delete_all_reminders(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: Interaction):
        self.value = False
        self.stop()



class reminder_delete(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import reminder

    ###reminder#delete###########################################################

    @reminder.subcommand(name = "delete", description = "delete a reminder from your reminder list")
    async def reminder_delete(self,
                              interaction: Interaction,
                              *,
                              reminder_id: str = SlashOption(description="the ID of the remidner to be deleted or 'ALL' (to find your reminder ID use '/reminder list'", required=True, min_length=1, max_length=10)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /reminder delete {reminder_id}")

        if reminder_id == "ALL":
            delete_id = reminder_id
        else:
            try:
                delete_id = int(reminder_id)
            except:
                await interaction.response.send_message(f"`{reminder_id}` isn't a valid reminder_id.", ephemeral=True)
                return

        deleted , deleted_all = delete_reminder(interaction.user.id, delete_id)

        

        if deleted_all == "ALL":
            view = question_delete_all_reminders()
            await interaction.response.send_message("Do you really want to delete **ALL** your __reminders__ (they can't be recovered)?", view=view, delete_after=30, ephemeral=True)
            await view.wait()

            if view.value is None:
                await interaction.user.send("Your __reminders__ have **not** been deleted! The buttons stopped working with this message.")
                return
            elif view.value:
                deleted_all = delete_all_user_reminders(interaction.user.id)

                if not deleted_all:
                    await interaction.user.send("You didn't have any __reminders__.")
                    return

                print(f"{interaction.user}: /reminder delete {reminder_id} went through")

                await interaction.user.send("**ALL** your __reminders__ have been deleted!")

                uses_update("command_uses", "reminder delete")
                return
            elif not view.value:
                await interaction.user.send("Your __reminders__ have **not** been deleted!")
                return



        if not deleted:
            await interaction.response.send_message(f"You don't have a reminder with the ID `{reminder_id}`.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your reminder with the ID `{reminder_id}` has been deleted.", ephemeral=True)

        uses_update("command_uses", "reminder delete")

def setup(client):
    client.add_cog(reminder_delete(client))