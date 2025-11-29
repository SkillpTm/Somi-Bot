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

        await interaction.response.defer(with_message=True)

        guild_with_counts = await self.client.fetch_guild(interaction.guild.id, with_counts=True)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP,
            image = interaction.guild.banner.url if interaction.guild.banner else "",
            title = f"Server: `{interaction.guild.name}`",
            footer = "Created:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = interaction.guild.created_at,
            fields = [
                EmbedField(
                    "ID:",
                    f"`{interaction.guild.id}`",
                    False
                ),
                EmbedField(
                    "Owner:",
                    interaction.guild.owner.mention,
                    True
                ),
                EmbedField(
                    "Boost Level:",
                    f"Level: `{interaction.guild.premium_tier}`\nBoosters: `{interaction.guild.premium_subscription_count}`",
                    True
                ),
                EmbedField(
                    "Members:",
                    f"Total: `{interaction.guild.member_count}`\nOnline: `{guild_with_counts.approximate_presence_count}`\nBots: `{len(interaction.guild.bots)}`",
                    True
                ),
                EmbedField(
                    "Channels:",
                    f"Text: `{len(interaction.guild.text_channels)}`\nVoice: `{len(interaction.guild.voice_channels)}`",
                    True
                ),
                EmbedField(
                    "Roles:",
                    f"Total: `{len(interaction.guild.roles)}`\nTop Role: {interaction.guild.roles[len(interaction.guild.roles)-1].mention}",
                    True
                ),
                EmbedField(
                    "Emojis:",
                    f"Static: `{(static_emotes_amount := len([emote for emote in interaction.guild.emojis if not emote.animated]))}/{interaction.guild.emoji_limit}`\nAnimated: `{len(interaction.guild.emojis) - static_emotes_amount}/{interaction.guild.emoji_limit}`",
                    True
                ),
                EmbedField(
                    "Stickers:",
                    f"Total: `{len(interaction.guild.stickers)}/{interaction.guild.sticker_limit}`",
                    True
                ),
                EmbedField(
                    "Description:",
                    interaction.guild.description or "",
                    False
                )
            ]
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Severinfo(client))