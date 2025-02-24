####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import CommandUsesDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class About(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "about", description = "tells you about Somi bot")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def about(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        """This command outputs various information about the bot to the user"""

        self.client.Loggers.action_log(Get().interaction_log_message(interaction, "/about"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"{self.client.user}",
            author_icon = self.client.user.display_avatar.url,
            title = "Information",
            description = f"""
                          {self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
                          Originally it was created to fullfil all needs of [Somicord]({self.client.SOMICORD_INVITE}).
                          """,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Created by:",
                    f"<@{self.client.owner_id}>",
                    True
                ],

                [
                    "Current Version:",
                    f"`{self.client.VERSION}`",
                    True
                ],

                [
                    "Uptime (since):",
                    f"<t:{self.client.start_time}:R>",
                    True
                ],

                [
                    "Servers:",
                    f"`{len(self.client.guilds)}`",
                    True
                ],

                [
                    "Visible Users:",
                    f"`{Get().visible_users(self.client)}`",
                    True
                ],

                [
                    "Global Command Executions:",
                    f"`{CommandUsesDB('command_uses').get_total()}`",
                    True
                ],

                [
                    "Invites:",
                    f"You can invite Somi using this [link]({self.client.SOMI_INVITE}). Additionally you can checkout Somi's code on [GitHub]({self.client.SOMI_GITHUB}).",
                    False
                ],

                [
                    "Issues:",
                    "You can report bugs and make suggestions by using /feedback!",
                    False
                ],

                [
                    "Data and Usage:",
                    f"Here you can find our [Terms of Service]({self.client.SOMI_TOS}) and [Privacy Policy]({self.client.SOMI_PP}). Additionally you're able to make inquiries at {self.client.SOMI_CONTACT_EMAIL}.",
                    False
                ]
            ]
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(About(client))