import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ReminderDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class ReminderList(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import reminder

    ####################################################################################################

    @reminder.subcommand(name = "list", description = "a list of all your reminders")
    @nextcord_AC.check(Checks.interaction_not_by_bot())
    async def reminder_list(self, interaction: nextcord.Interaction) -> None:
        """This command will list all reminders of a user"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/reminder list"))

        user_reminders = ReminderDB(interaction.user.id).get_list()

        if not user_reminders:
            await interaction.response.send_message(embed=EmbedFunctions().error("You don't have any reminders.\nTo add a reminder use `/reminder add`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        output = ""

        #TODO add pages to this
        for reminder in user_reminders:
            output += f"<t:{reminder[0]}:F> // ID: {reminder[2]} - [Link]({reminder[1]})\nReminder: `{reminder[3][:30]}"

            if len(reminder[3]) > 30:
                output += "..."

            output += "`\n\n"

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"Reminder List for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderList(client))