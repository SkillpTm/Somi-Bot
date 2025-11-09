import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.utilities import SomiBot



class ReminderList(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.reminder.subcommand(Commands().data["reminder list"].name, Commands().data["reminder list"].description)
    async def reminder_list(self, interaction: nextcord.Interaction) -> None:
        """This command will list all reminders of a user"""

        if not (user_reminders := await (await DBHandler(self.client.database, user_id=interaction.user.id).reminder()).get_list()):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You don't have any reminders.\nTo add a reminder use `/reminder add`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        output = ""

        for reminder in user_reminders:
            output += f"<t:{reminder[0]}:F> // ID: {reminder[2]} - [Link]({reminder[1]})\nReminder: `{reminder[3][:30]}"

            if len(reminder[3]) > 30:
                output += "..."

            output += "`\n\n"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Reminder List for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            description = output
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderList(client))