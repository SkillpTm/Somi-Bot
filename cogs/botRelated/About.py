import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class About(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="about", description="tells you about Somi bot")
    async def about(self, interaction: nextcord.Interaction) -> None:
        """This command outputs various information about the bot to the user"""

        self.client.logger.action_log(Get.log_message(interaction, "/about"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.config.BOT_COLOR,
            author = f"{self.client.user}",
            author_icon = self.client.user.display_avatar.url,
            title = "Information",
            description = f"""
                          {self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
                          Originally it was created to fullfil all needs of [Somicord]({self.client.config.SOMICORD_INVITE}).
                          Additionally you can checkout Somi's source code on [GitHub]({self.client.config.BOT_GITHUB}).
                          """,
            fields = [
                [
                    "Created by:",
                    f"<@{self.client.owner_id}>",
                    True
                ],

                [
                    "Current Version:",
                    f"`{self.client.config.VERSION}`",
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
                    "Visible Users:",
                    f"`{len(self.client.visible_users())}`",
                    True
                ],

                [
                    "Global Command Executions:",
                    f"`{await (await DBHandler(self.client.database).telemetry()).get_total_amount()}`",
                    True
                ],

                [
                    "Invites:",
                    f"You can invite Somi using this [link]({self.client.config.BOT_INVITE}) and her support server can be found [here]({self.client.config.SUPPORT_SERVER_INVITE}).",
                    False
                ],

                [
                    "Issues:",
                    "You can report bugs and make suggestions by using /feedback!",
                    False
                ],

                [
                    "Data and Usage:",
                    f"Here you can find our [Terms of Service]({self.client.config.BOT_TOS}) and [Privacy Policy]({self.client.config.BOT_PP}).",
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(About(client))