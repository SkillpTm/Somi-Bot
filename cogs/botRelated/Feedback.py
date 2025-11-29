import datetime
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config, Logger
from lib.modules import SomiBot


class FeedbackModal(nextcord.ui.Modal):

    def __init__(self, client: SomiBot) -> None:
        super().__init__("Please submit your feedback down below!", timeout=None)
        self.client = client

        self.feedback: nextcord.ui.TextInput[typing.Any] = nextcord.ui.TextInput(
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
        interaction: nextcord.Interaction[SomiBot]
    ) -> None:
        """Submits the feedback to the db"""

        if not interaction.user:
            return

        Logger().action_log(interaction, "/feedback", {"submission": self.feedback.value or ""}) # type: ignore

        if interaction.guild:
            server_id = interaction.guild.id
            origin_text = f"Feedback from server: `{interaction.guild.name}` | `({interaction.guild.id})`:"
        else:
            server_id = 0 # DMs are indecated by a 0
            origin_text = "Feedback from a private channel:"

        await db.Feedback._.add({
            db.Feedback.SERVER: server_id,
            db.Feedback.USER: interaction.user.id,
            db.Feedback.TIME: datetime.datetime.now().strftime("Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"),
            db.Feedback.MESSAGE: self.feedback.value
        })

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            title = f"Feedback by: `{interaction.user.name}` | `({interaction.user.id})`",
            thumbnail = interaction.user.display_avatar.url,
            description = f"{origin_text}\n{self.feedback.value}"
        )

        await self.client.get_channel(Config().SUPPORT_SERVER_FEEDBACK_ID).send(embed=embed) # type: ignore
        await interaction.send(embed=EmbedFunctions.get_success_message("Your feedback has been submitted!"), ephemeral=True)



class Feedback(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["feedback"].name,
        Commands().data["about"].description,
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def feedback(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """Sends out a modal to receive feedback"""

        await interaction.response.send_modal(FeedbackModal(self.client))



def setup(client: SomiBot) -> None:
    client.add_cog(Feedback(client))