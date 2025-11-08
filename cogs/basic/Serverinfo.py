import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Config
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Severinfo(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "si",
        description = "gives information about this server",
        name_localizations = {country_tag:"serverinfo" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def serverinfo(self, interaction: nextcord.Interaction) -> None:
        """This command gives you infomration about a server"""

        await interaction.response.defer(with_message=True)

        guild_with_counts = await self.client.fetch_guild(interaction.guild.id, with_counts=True)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP,
            title = f"Server Information: `{interaction.guild.name}`",
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
                    f"Total: `{guild_with_counts.approximate_member_count}`\nOnline: `{guild_with_counts.approximate_presence_count}`",
                    True
                ],

                [
                    "Channels:",
                    f"Text: `{len(interaction.guild.text_channels)}`\nVoice: `{len(interaction.guild.voice_channels)}`",
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(interaction.guild.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Boost Level:",
                    f"Level: `{interaction.guild.premium_tier}`\nBoosters: `{interaction.guild.premium_subscription_count}`",
                    True
                ],

                [
                    "Vanity Invite:",
                    (await interaction.guild.vanity_invite()).url if "VANITY_URL" in interaction.guild.features else "",
                    True
                ],

                [
                    "Description:",
                    interaction.guild.description,
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Severinfo(client))