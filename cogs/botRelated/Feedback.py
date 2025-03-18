import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
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

        self.client.Loggers.action_log(Get.log_message(interaction, "/feedback", {"submission": self.feedback.value}))

        if interaction.guild:
            server_id = interaction.guild.id
            origin_text = f"Feedback from server: `{interaction.guild.name}` | `({interaction.guild.id})`:"
        else:
            server_id = 0 # DMs are indecated by a 0
            origin_text = f"Feedback from DM channel:"

        await (await DBHandler(self.client.PostgresDB, server_id, interaction.user.id).feedback()).submit(Get.kst_timestamp(), self.feedback.value)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            title = f"Feedback by: `{interaction.user.name}` | `({interaction.user.id})`",
            thumbnail = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            description = f"{origin_text}\n{self.feedback.value}"
        )

        await self.client.get_channel(self.client.SUPPORT_SERVER_FEEDBACK_ID).send(embed=embed)
        await interaction.response.send_message(embed=EmbedFunctions().get_success_message("Your feedback has been submitted!"), ephemeral=True)



class Feedback(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "feedback", description = "give feedback to the bot, with a suggestion or submit a bug-report")
    async def feedback(self, interaction: nextcord.Interaction) -> None:

        self.client.Loggers.action_log(Get.log_message(interaction, "/feedback"))

        modal = FeedbackModal(self.client)
        await interaction.response.send_modal(modal=modal)



def setup(client: SomiBot) -> None:
    client.add_cog(Feedback(client))