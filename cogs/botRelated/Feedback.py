####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import FeedbackDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot


class FeedbackModal(nextcord.ui.Modal):

    def __init__(self, client) -> None:
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

    async def callback(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        """Submits the feedback to the db"""

        self.client.Loggers.action_log(Get().interaction_log_message(interaction, "/feedback"), {"submission": self.feedback.value})

        #TODO send this response into the support server
        FeedbackDB().add(interaction.guild.id, interaction.user.id, str(interaction.user), Get().kst_timestamp(), self.feedback.value)

        await interaction.response.send_message(embed=EmbedFunctions().success("Your feedback has been submitted!"), ephemeral=True)



class Feedback(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "feedback", description = "give feedback to the bot, with a suggestion or submit a bug-report")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def feedback(self, interaction: nextcord.Interaction) -> None:

        self.client.Loggers.action_log(Get().interaction_log_message(interaction, "/feedback"))

        modal = FeedbackModal(self.client)
        await interaction.response.send_modal(modal=modal)



def setup(client: SomiBot) -> None:
    client.add_cog(Feedback(client))