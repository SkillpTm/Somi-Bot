import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class ReminderList(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.reminder.subcommand(Commands().data["reminder list"].name, Commands().data["reminder list"].description)
    async def reminder_list(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command will list all reminders of a user"""

        output = ""

        async for entry in db.Reminder._.get_multiple(where={db.Reminder.USER: interaction.user.id}, order_by=db.Reminder.TIME):
            reminder_text = str(db.Reminder.MESSAGE.retrieve(entry))
            reminder_text = f"{reminder_text[:30]}..." if len(reminder_text) > 30 else reminder_text
            output += f"<t:{db.Reminder.TIME.retrieve(entry)}:F> // ID: {db.Reminder.ID.retrieve(entry)} - [Link]({db.Reminder.LINK.retrieve(entry)})\nReminder: `{reminder_text}`\n\n"

        if not output:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You don't have any reminders.\nTo add a reminder use `/reminder add`."), ephemeral=True)
            return

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Reminder List for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            description = output
        )

        await interaction.response.send_message(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderList(client))