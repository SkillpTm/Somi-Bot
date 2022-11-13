###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_feedback import submit_feedback
from utilities.maincommands import checks
from utilities.partial_commands import get_kst_time_stamp



class FeedbackModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Please submit your feedback down below!", timeout=None)

        self.feedback: str = nextcord.ui.TextInput(
            label="Feedback:",
            style=nextcord.TextInputStyle.paragraph,
            min_length=1,
            max_length=4000,
            placeholder="write your feedback here",
            required=True)

        self.add_item(self.feedback)

    async def callback(self, interaction: Interaction):
        kst_timestamp = get_kst_time_stamp(source = "/feedback")

        print(f"{interaction.user}: /feedback submission:\n{self.feedback.value}")

        server_id = interaction.guild.id
        user_id = interaction.user.id
        user_name = str(interaction.user)
        submission_time = kst_timestamp
        feedback = self.feedback.value

        submit_feedback(server_id, user_id, user_name.replace("'", "‘"), submission_time, feedback.replace("'", "‘"))

        await interaction.response.send_message("Your feedback has been submitted!", ephemeral=True)

        uses_update("command_uses", "feedback")

        return

class feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###feedback###########################################################

    @nextcord.slash_command(name = "feedback", description = "give feedback to the bot, with a suggestion or submit a bug-report")
    async def feedback(self,
                   interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /feedback")

        FeedbackModalVariable = FeedbackModal()
        await interaction.response.send_modal(modal=FeedbackModalVariable)

def setup(client):
    client.add_cog(feedback(client))