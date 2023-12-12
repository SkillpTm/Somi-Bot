####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import CommandUsesDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class About(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "about", description = "tells you about Somi bot")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def about(self,
                    interaction: nextcord.Interaction):
        """This command outputs various information about the bot to the user"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /about")

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
                    "Uptime:",
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
                    f"`{CommandUsesDB().get_total_uses('command_uses')}`",
                    True
                ],

                [
                    "Invites:",
                    "Currently there are no plans to have public invites. You might get an invite by asking `skillp`.",
                    False
                ],

                [
                    "Issues:",
                    "You can report bugs and make suggestions by using /feedback!",
                    False
                ]
            ]
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot):
    client.add_cog(About(client))