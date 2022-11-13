###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

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

    async def callback(self,
                       interaction: nextcord.Interaction):
        kst_timestamp = get_kst_time_stamp(source = "/feedback")

        print(f"{interaction.user}: /feedback submission:\n{self.feedback.value}")

        submit_feedback(interaction.guild.id, interaction.user.id, str(interaction.user).replace("'", "‘"), kst_timestamp, self.feedback.value.replace("'", "‘"))

        await interaction.response.send_message("Your feedback has been submitted!", ephemeral=True)

        uses_update("command_uses", "feedback")

class Feedback(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###feedback###########################################################

    @nextcord.slash_command(name = "feedback", description = "give feedback to the bot, with a suggestion or submit a bug-report")
    async def feedback(self,
                       interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /feedback")

        feedback_modal = FeedbackModal()
        await interaction.response.send_modal(modal=feedback_modal)



def setup(client):
    client.add_cog(Feedback(client))