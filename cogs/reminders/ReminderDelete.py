###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_reminders import delete_reminder, delete_all_user_reminders, list_reminder
from utilities.maincommands import checks
from utilities.partial_commands import string_search_to_list, deactivate_view_children



class QuestionDeleteAllReminders(nextcord.ui.View):
    def __init__(self, interaction):
        self.interaction: nextcord.Interaction = interaction
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def on_timeout(self):
        await deactivate_view_children(self)



class ReminderDelete(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import reminder

    ###reminder#delete###########################################################

    @reminder.subcommand(name = "delete", description = "delete a reminder from your reminder list")
    async def reminder_delete(self,
                              interaction: nextcord.Interaction,
                              *,
                              reminder_id: str = nextcord.SlashOption(description="the ID of the remidner to be deleted or 'ALL' (to find your reminder ID use '/reminder list'", required=True, min_length=1, max_length=10)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /reminder delete {reminder_id}")

        if reminder_id == "ALL":
            delete_id = reminder_id

        elif not reminder_id.isdigit():
            await interaction.response.send_message(f"`{reminder_id}` isn't a valid reminder_id.", ephemeral=True)
            return

        deleted = delete_reminder(interaction.user.id, delete_id)

        

        if deleted_all == "ALL":
            view = QuestionDeleteAllReminders(interaction)
            await interaction.response.send_message("Do you really want to delete **ALL** your __reminders__ (they can't be recovered)?", view=view, ephemeral=True)
            await view.wait()

            if view.value is None or not view.value:
                await interaction.followup.send("Your __reminders__ have **not** been deleted!", ephemeral=True)
                return
            elif view.value:
                deleted_all = delete_all_user_reminders(interaction.user.id)

                if not deleted_all:
                    await interaction.followup.send("You don't have any __reminders__ to be deleted.")
                    return

                print(f"{interaction.user}: /reminder delete {reminder_id} went through")

                await interaction.followup.send("**ALL** your __reminders__ have been deleted!")

                uses_update("command_uses", "reminder delete")
                return



        if not deleted:
            await interaction.response.send_message(f"You don't have a reminder with the ID `{reminder_id}`.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your reminder with the ID `{reminder_id}` has been deleted.", ephemeral=True)

        uses_update("command_uses", "reminder delete")

    @reminder_delete.on_autocomplete("reminder_id")
    async def autocomplete_reminder_delete(self,
                                           interaction: nextcord.Interaction,
                                           reminder_id: str):
        reminder_times, bot_reply_links, delete_ids, clean_reminders = list_reminder(interaction.user.id)

        autocomplete_list = string_search_to_list(reminder_id, delete_ids)

        await interaction.response.send_autocomplete(autocomplete_list)



def setup(client):
    client.add_cog(ReminderDelete(client))