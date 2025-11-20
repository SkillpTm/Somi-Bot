import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Severinfo(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["serverinfo"].alias,
        Commands().data["serverinfo"].description,
        name_localizations = {country_tag: Commands().data["serverinfo"].name for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def serverinfo(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command gives you infomration about a server"""

        if not interaction.guild:
            return

        await interaction.response.defer(with_message=True)

        guild_with_counts = await self.client.fetch_guild(interaction.guild.id, with_counts=True)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP,
            title = f"Server Information: `{interaction.guild.name}`",
            fields = [
                EmbedField(
                    "ID:",
                    str(interaction.guild.id),
                    False
                ),
                EmbedField(
                    "Owner:",
                    interaction.guild.owner.mention,
                    True
                ),
                EmbedField(
                    "Members:",
                    f"Total: `{guild_with_counts.approximate_member_count}`\nOnline: `{guild_with_counts.approximate_presence_count}`",
                    True
                ),
                EmbedField(
                    "Channels:",
                    f"Text: `{len(interaction.guild.text_channels)}`\nVoice: `{len(interaction.guild.voice_channels)}`",
                    True
                ),
                EmbedField(
                    "Created at:",
                    f"<t:{int(time.mktime(interaction.guild.created_at.timetuple()))}>",
                    True
                ),
                EmbedField(
                    "Boost Level:",
                    f"Level: `{interaction.guild.premium_tier}`\nBoosters: `{interaction.guild.premium_subscription_count}`",
                    True
                ),
                EmbedField(
                    "Vanity Invite:",
                    vanity.url if (vanity := await interaction.guild.vanity_invite()) else "",
                    True
                ),
                EmbedField(
                    "Description:",
                    interaction.guild.description or "",
                    False
                )
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Severinfo(client))