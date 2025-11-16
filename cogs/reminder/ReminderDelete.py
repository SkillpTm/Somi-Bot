import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db, Order
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot, YesNoButtons

class ReminderDelete(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.reminder.subcommand(Commands().data["reminder delete"].name, Commands().data["reminder delete"].description)
    async def reminder_delete(
        self,
        interaction: nextcord.Interaction,
        *,
        reminder_id: str = nextcord.SlashOption(
            Commands().data["reminder delete"].parameters["reminder_id"].name,
            Commands().data["reminder delete"].parameters["reminder_id"].description,
            required = True,
            min_length = 9,
            max_length = 9
        )
    ) -> None:
        """This command let's you delete a reminder with it's ID or all reminders with 'ALL'"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not await db.Reminder._.get_all(where={db.Reminder.USER: interaction.user.id}):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You don't have any reminders to be deleted!"), ephemeral=True)
            return

        if reminder_id == "DELETE_ALL":
            self.delete_all(interaction)
            return


        if not reminder_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"`{reminder_id}` isn't a valid reminder id."), ephemeral=True)
            return

        if not await db.Reminder._.delete({db.Reminder.ID: reminder_id, db.Reminder.USER: interaction.user.id}):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"You don't have a reminder with the ID `{reminder_id}`.\nTo get a list of your reminders use `/reminder list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Your reminder `{reminder_id}` has been deleted."), ephemeral=True)

    ####################################################################################################

    async def delete_all(self, interaction: nextcord.Interaction) -> None:
        """asks the user if they want to delete all their reminders and does as answered"""

        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().get_info_message("Do you really want to delete **ALL** your reminders __**(they can't be recovered)?**__"), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("Your reminders have **not** been deleted!"), ephemeral=True)
            return

        await db.Reminder._.delete({db.Reminder.USER: interaction.user.id})

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("**ALL** your reminders have been deleted!"))
        return

    ####################################################################################################

    @reminder_delete.on_autocomplete("reminder_id")
    async def reminder_delete_autocomplete_reminder_id(
        self,
        interaction: nextcord.Interaction,
        reminder_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        reminders = {}

        async for entry in db.Reminder._.get_multiple(where={db.Reminder.USER: interaction.user.id}, order_by=db.Reminder.TIME, order=Order.ASCENDING):
            reminder_text: str = db.Reminder.MESSAGE.retrieve(entry)
            reminder_text = f"{reminder_text[:30]}..." if len(reminder_text) > 30 else reminder_text

            reminders.update({f"{db.Reminder.ID.retrieve(entry)}: {reminder_text}" : db.Reminder.ID.retrieve(entry)})

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                reminder_id,
                reminders
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderDelete(client))