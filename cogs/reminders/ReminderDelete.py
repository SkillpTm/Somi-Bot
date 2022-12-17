####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ReminderDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot, YesNoButtons

class ReminderDelete(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import reminder

    ####################################################################################################

    @reminder.subcommand(name = "delete", description = "delete a reminder from your reminder list")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def reminder_delete(self,
                              interaction: nextcord.Interaction,
                              *,
                              reminder_id: str = nextcord.SlashOption(description="the ID of the remidner to be deleted or 'ALL' (to find your reminder ID use '/reminder list'", required=True, min_length=1, max_length=10)):
        """This command let's you delete a reminder with it's ID or all reminders with 'ALL'"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /reminder delete {reminder_id}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        user_reminders = ReminderDB().user_list(interaction.user.id)

        if user_reminders == []:
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any reminders to be deleted!"), ephemeral=True)
            return

        if not reminder_id.isdigit() and reminder_id != "ALL":
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{reminder_id}` isn't a valid reminder id."), ephemeral=True)
            return

        deleted = ReminderDB().delete(interaction.user.id, reminder_id)

        

        if deleted == "ALL":
            view = YesNoButtons(interaction=interaction)
            await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to delete **ALL** your reminders __**(they can't be recovered)?**__", self.client), view=view, ephemeral=True)
            await view.wait()

            if not view.value:
                await interaction.followup.send(embed=EmbedFunctions().error("Your reminders have **not** been deleted!"), ephemeral=True)
                return
                
            elif view.value:
                ReminderDB().delete_all(interaction.user.id)

                self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /reminder delete {reminder_id} went through")

                await interaction.followup.send(embed=EmbedFunctions().success("**ALL** your reminders have been deleted!"))
                return



        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You don't have a reminder with the ID `{reminder_id}`.\nTo get a list of your reminders use `/reminder list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"Your reminder `{reminder_id}` has been deleted."), ephemeral=True)

    ####################################################################################################

    @reminder_delete.on_autocomplete("reminder_id")
    async def autocomplete_reminder_delete(self,
                                           interaction: nextcord.Interaction,
                                           reminder_id: str):
        user_reminders = ReminderDB().user_list(interaction.user.id)
        delete_ids = {}

        for reminder in user_reminders:
            if len(reminder[3]) > 30:
                reminder_text = f"{reminder[3][:30]}..."
            else:
                reminder_text = f"{reminder[3]}"
            delete_ids.update({f"{reminder[2]}: {reminder_text}" : reminder[2]})

        autocomplete_dict = Get().autocomplete_dict_from_search_string(reminder_id, delete_ids)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(ReminderDelete(client))