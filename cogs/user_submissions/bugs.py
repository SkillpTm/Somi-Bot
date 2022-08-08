###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_bugs_suggestions import submit_bug_report
from utilities.maincommands import checks
from utilities.partial_commands import get_kst_time_stamp



class BugReportModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Please submit your bug-report down below!", timeout=None)

        self.bug: str = nextcord.ui.TextInput(
            label="Bug-Report:",
            style=nextcord.TextInputStyle.paragraph,
            min_length=1,
            max_length=4000,
            placeholder="write your bug-report here",
            required=True)

        self.add_item(self.bug)

    async def callback(self, interaction: Interaction):
        kst_timestamp = get_kst_time_stamp(source = "/bugs")

        print(f"{interaction.user}: /bugs submission:\n{self.bug.value}")

        server_id = interaction.guild.id
        user_id = interaction.user.id
        user_name = str(interaction.user)
        submission_time = kst_timestamp
        bug_report = self.bug.value

        submit_bug_report(server_id, user_id, user_name.replace("'", "‘"), submission_time, bug_report.replace("'", "‘"))

        await interaction.response.send_message("Your bug-report has been submitted!", ephemeral=True)

        uses_update("command_uses", "bugs")

        return

class bugs(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###bugs###########################################################

    @nextcord.slash_command(name = "bugs", description = "Report a bug")
    async def bugs(self,
                   interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /bugs")

        BugModal = BugReportModal()
        await interaction.response.send_modal(modal=BugModal)

def setup(client):
    client.add_cog(bugs(client))