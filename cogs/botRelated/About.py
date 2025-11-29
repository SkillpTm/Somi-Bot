import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class About(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["about"].name,
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
    async def about(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command outputs various information about the bot to the user"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            author = f"{self.client.user}",
            author_icon = self.client.user.display_avatar.url,
            title = "Information",
            footer = "Created:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = self.client.user.created_at,
            description = f"""
                          {self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
                          Originally it was created to fullfil all needs of [Somicord]({Config().SOMICORD_INVITE}).
                          Additionally you can checkout Somi's source code on [GitHub]({Config().BOT_GITHUB}).
                          """,
            fields = [
                EmbedField(
                    "Created by:",
                    f"<@{self.client.owner_id}>",
                    True
                ),
                EmbedField(
                    "Current Version:",
                    f"`{Config().VERSION}`",
                    True
                ),
                EmbedField(
                    "Up Since:",
                    f"<t:{self.client.start_time}:f>",
                    True
                ),
                EmbedField(
                    "Servers:",
                    f"`{len(self.client.guilds)}`",
                    True
                ),
                EmbedField(
                    "Users:",
                    f"`{len(self.client.users)}`",
                    True
                ),
                EmbedField(
                    "Global Command Executions:",
                    f"`{sum(typing.cast(list[int], await db.Telemetry.AMOUNT.get_all()))}`",
                    True
                ),
                EmbedField(
                    "Invites:",
                    f"You can invite Somi using this [link]({Config().BOT_INVITE}) and her support server can be found [here]({Config().SUPPORT_SERVER_INVITE}).",
                    False
                ),
                EmbedField(
                    "Issues:",
                    "You can report bugs and make suggestions by using /feedback!",
                    False
                ),
                EmbedField(
                    "Data and Usage:",
                    f"Here you can find our [Terms of Service]({Config().BOT_TOS}) and [Privacy Policy]({Config().BOT_PP}).",
                    False
                )
            ]
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(About(client))