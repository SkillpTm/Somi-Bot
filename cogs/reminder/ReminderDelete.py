import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ReminderDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot, YesNoButtons

class ReminderDelete(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import reminder

    ####################################################################################################

    @reminder.subcommand(name = "delete", description = "delete a reminder from your reminder list")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def reminder_delete(
        self,
        interaction: nextcord.Interaction,
        *,
        reminder_id: str = nextcord.SlashOption(
            description = "the ID of the remidner to be deleted or 'DELETE_ALL' (to find your reminder ID use '/reminder list'",
            required = True,
            min_length = 1,
            max_length = 10
        )
    ) -> None:
        """This command let's you delete a reminder with it's ID or all reminders with 'ALL'"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/reminder delete",
            {"reminder_id": reminder_id}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not ReminderDB(interaction.user.id).get_list():
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any reminders to be deleted!"), ephemeral=True)
            return


        if reminder_id == "DELETE_ALL":
            self.delete_all(interaction)
            return


        if not reminder_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{reminder_id}` isn't a valid reminder id."), ephemeral=True)
            return

        deleted = ReminderDB(interaction.user.id).delete(reminder_id)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You don't have a reminder with the ID `{reminder_id}`.\nTo get a list of your reminders use `/reminder list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"Your reminder `{reminder_id}` has been deleted."), ephemeral=True)

    ####################################################################################################

    @reminder_delete.on_autocomplete("reminder_id")
    async def autocomplete_reminder_delete(
        self,
        interaction: nextcord.Interaction,
        reminder_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        valid_ids = {}

        for reminder in ReminderDB(interaction.user.id).get_list():
            reminder_text = f"{reminder[3][:30]}"
            
            if len(reminder[3]) > 30:
                reminder_text += "..."

            valid_ids.update({f"{reminder[2]}: {reminder_text}" : reminder[2]})

        autocomplete_dict = Get().autocomplete_dict_from_search_string(reminder_id, valid_ids)

        await interaction.response.send_autocomplete(autocomplete_dict)

    ####################################################################################################

    async def delete_all(self, interaction: nextcord.Interaction) -> None:
        """asks the user if they want to delete all their reminders and does as answered"""
    
        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to delete **ALL** your reminders __**(they can't be recovered)?**__", self.client), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().error("Your reminders have **not** been deleted!"), ephemeral=True)
            return
            
        ReminderDB(interaction.user.id).delete_all()

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/reminder delete",
            {"DELETE_ALL": "deleted"}
        ))

        await interaction.followup.send(embed=EmbedFunctions().success("**ALL** your reminders have been deleted!"))
        return



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderDelete(client))