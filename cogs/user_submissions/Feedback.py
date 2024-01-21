####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import FeedbackDB
from lib.modules import Checks, Get
from lib.utilities import SomiBot


class FeedbackModal(nextcord.ui.Modal):
    def __init__(self, client):
        super().__init__("Please submit your feedback down below!", timeout=None)
        self.client: SomiBot = client

        self.feedback = nextcord.ui.TextInput(
            label = "Feedback:",
            style = nextcord.TextInputStyle.paragraph,
            min_length = 1,
            max_length = 4000,
            placeholder = "write your feedback here",
            required = True
        )

        self.add_item(self.feedback)

    async def callback(self,
                       interaction: nextcord.Interaction):
        """Submits the feedback to the db"""
        
        kst_time = Get().kst_timestamp(source = "/feedback")

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /feedback submission:\n{self.feedback.value}")

        FeedbackDB().add(interaction.guild.id, interaction.user.id, str(interaction.user), kst_time, self.feedback.value)

        await interaction.response.send_message("Your feedback has been submitted!", ephemeral=True)



class Feedback(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "feedback", description = "give feedback to the bot, with a suggestion or submit a bug-report")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def feedback(self,
                       interaction: nextcord.Interaction):

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /feedback")

        modal = FeedbackModal(self.client)
        await interaction.response.send_modal(modal=modal)



def setup(client: SomiBot):
    client.add_cog(Feedback(client))