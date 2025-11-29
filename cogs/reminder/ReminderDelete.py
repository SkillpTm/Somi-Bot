import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Order
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot, YesNoButtons

class ReminderDelete(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.reminder.subcommand(Commands().data["reminder delete"].name, Commands().data["reminder delete"].description)
    async def reminder_delete(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        reminder_id: str = nextcord.SlashOption(
            Commands().data["reminder delete"].parameters["reminder_id"].name,
            Commands().data["reminder delete"].parameters["reminder_id"].description,
            required = False,
            min_length = 9,
            max_length = 9
        ),
        delete_all: typing.Literal["Yes", ""] = nextcord.SlashOption(
            Commands().data["reminder delete"].parameters["delete_all"].name,
            Commands().data["reminder delete"].parameters["delete_all"].description,
            required = False,
            choices = ["Yes"],
            min_length = 2,
            max_length = 50,
            default = ""
        )
    ) -> None:
        """This command let's you delete a reminder with it's ID or all reminders with 'ALL'"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not reminder_id and not delete_all:
            await interaction.send(embed=EmbedFunctions.get_error_message("Please either provide an ID or choose to delete all your reminders."))
            return

        if not await db.Reminder._.get_all(where={db.Reminder.USER: interaction.user.id}):
            await interaction.send(embed=EmbedFunctions.get_error_message("You don't have any reminders to be deleted!"))
            return

        if delete_all == "Yes":
            await self.delete_all(interaction)
            return


        if not reminder_id.isdigit():
            await interaction.send(embed=EmbedFunctions.get_error_message(f"`{reminder_id}` isn't a valid reminder id."))
            return

        if not await db.Reminder._.delete({db.Reminder.ID: reminder_id, db.Reminder.USER: interaction.user.id}):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"You don't have a reminder with the ID `{reminder_id}`.\nTo get a list of your reminders use `/reminder list`."), ephemeral=True)
            return

        await interaction.send(embed=EmbedFunctions.get_success_message(f"Your reminder `{reminder_id}` has been deleted."))


    async def delete_all(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """asks the user if they want to delete all their reminders and does as answered"""

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions.get_info_message("Do you really want to delete **ALL** your reminders __**(they can't be recovered)?**__"), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions.get_error_message("Your reminders have **not** been deleted!"))
            return

        await db.Reminder._.delete({db.Reminder.USER: interaction.user.id}, limit=1_000_000)

        await interaction.send(embed=EmbedFunctions.get_success_message("**ALL** your reminders have been deleted!"))
        return


    @reminder_delete.on_autocomplete("reminder_id")
    async def reminder_delete_autocomplete_reminder_id(
        self,
        interaction: nextcord.Interaction[SomiBot],
        reminder_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        reminders = {}

        async for entry in db.Reminder._.get_multiple(where={db.Reminder.USER: interaction.user.id}, order_by=db.Reminder.TIME, order=Order.ASCENDING):
            reminders.update({f"{db.Reminder.ID.retrieve(entry)}: {db.Reminder.MESSAGE.retrieve(entry)}" : db.Reminder.ID.retrieve(entry)})

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                reminder_id,
                reminders
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderDelete(client))