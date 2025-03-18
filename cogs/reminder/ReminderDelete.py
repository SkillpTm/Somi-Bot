import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot, YesNoButtons

class ReminderDelete(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.reminder.subcommand(name = "delete", description = "delete a reminder from your reminder list")
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

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/reminder delete",
            {"reminder_id": reminder_id}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).reminder()).get_list():
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any reminders to be deleted!"), ephemeral=True)
            return


        if reminder_id == "DELETE_ALL":
            self.delete_all(interaction)
            return


        if not reminder_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{reminder_id}` isn't a valid reminder id."), ephemeral=True)
            return

        if not await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).reminder()).delete():
            await interaction.followup.send(embed=EmbedFunctions().error(f"You don't have a reminder with the ID `{reminder_id}`.\nTo get a list of your reminders use `/reminder list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"Your reminder `{reminder_id}` has been deleted."), ephemeral=True)

    ####################################################################################################

    @reminder_delete.on_autocomplete("reminder_id")
    async def reminder_delete_autocomplete_reminder_id(
        self,
        interaction: nextcord.Interaction,
        reminder_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        valid_ids = {}

        for reminder in await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).reminder()).get_list():
            reminder_text = f"{reminder[3][:30]}"
            
            if len(reminder[3]) > 30:
                reminder_text += "..."

            valid_ids.update({f"{reminder[2]}: {reminder_text}" : reminder[2]})

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                reminder_id,
                valid_ids
            )
        )

    ####################################################################################################

    async def delete_all(self, interaction: nextcord.Interaction) -> None:
        """asks the user if they want to delete all their reminders and does as answered"""
    
        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to delete **ALL** your reminders __**(they can't be recovered)?**__", self.client), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().error("Your reminders have **not** been deleted!"), ephemeral=True)
            return
            
        await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).reminder()).delete_all()

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/reminder delete",
            {"DELETE_ALL": "deleted"}
        ))

        await interaction.followup.send(embed=EmbedFunctions().success("**ALL** your reminders have been deleted!"))
        return



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderDelete(client))