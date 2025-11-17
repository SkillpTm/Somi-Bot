import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class About(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    @nextcord.slash_command(Commands().data["about"].name, Commands().data["about"].description)
    async def about(self, interaction: nextcord.Interaction) -> None:
        """This command outputs various information about the bot to the user"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"{self.client.user}",
            author_icon = self.client.user.display_avatar.url,
            title = "Information",
            description = f"""
                          {self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
                          Originally it was created to fullfil all needs of [Somicord]({Config().SOMICORD_INVITE}).
                          Additionally you can checkout Somi's source code on [GitHub]({Config().BOT_GITHUB}).
                          """,
            fields = [
                [
                    "Created by:",
                    f"<@{self.client.owner_id}>",
                    True
                ],

                [
                    "Current Version:",
                    f"`{Config().VERSION}`",
                    True
                ],

                [
                    "Up Since:",
                    f"<t:{self.client.start_time}:f>",
                    True
                ],

                [
                    "Servers:",
                    f"`{len(self.client.guilds)}`",
                    True
                ],

                [
                    "Users:",
                    f"`{len(self.client.users)}`",
                    True
                ],

                [
                    "Global Command Executions:",
                    f"`{sum(await db.Telemetry.AMOUNT.get_all())}`",
                    True
                ],

                [
                    "Invites:",
                    f"You can invite Somi using this [link]({Config().BOT_INVITE}) and her support server can be found [here]({Config().SUPPORT_SERVER_INVITE}).",
                    False
                ],

                [
                    "Issues:",
                    "You can report bugs and make suggestions by using /feedback!",
                    False
                ],

                [
                    "Data and Usage:",
                    f"Here you can find our [Terms of Service]({Config().BOT_TOS}) and [Privacy Policy]({Config().BOT_PP}).",
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(About(client))