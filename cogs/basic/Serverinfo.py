####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import time


####################################################################################################

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Severinfo(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################
        
    @nextcord.slash_command(name = "si", description = "gives information about this server", name_localizations = {country_tag:"serverinfo" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def serverinfo(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        """This command gives you infomration about a server"""

        self.client.Loggers.action_log(Get().interaction_log_message(interaction, "/serverinfo"))

        await interaction.response.defer(with_message=True)

        guild_with_counts = await self.client.fetch_guild(interaction.guild.id, with_counts=True)

        if interaction.guild.icon:
            server_icon_url = interaction.guild.icon
        else:
            server_icon_url = self.client.DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            thumbnail = server_icon_url,
            title = f"Server Information: `{interaction.guild.name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "ID:",
                    interaction.guild.id,
                    False
                ],
                
                [
                    "Owner:",
                    interaction.guild.owner.mention,
                    True
                ],

                [
                    "Members:",
                    f"Total: {guild_with_counts.approximate_member_count}\nOnline: {guild_with_counts.approximate_presence_count}",
                    True
                ],

                [
                    "Channels:",
                    f"Text: {len(interaction.guild.text_channels)}\nVoice: {len(interaction.guild.voice_channels)}",
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(interaction.guild.created_at.timetuple()))}>",
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Severinfo(client))