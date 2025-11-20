import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, LevelRoles
from lib.managers import Commands, Config
from lib.modules import SomiBot



class LevelsOverview(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.levels.subcommand(
        Commands().data["levels overview"].alias,
        Commands().data["levels overview"].description,
        name_localizations = {country_tag: Commands().data["levels overview"].name for country_tag in nextcord.Locale}
    )
    async def levels_overview(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """Displays information about levels and (if existing) shows a list of the levelroles/ignore channels"""

        await interaction.response.defer(with_message=True)

        output_role_list = await LevelRoles.get_level_range_with_role(interaction.guild) # type: ignore

        if not (output_ignore_channels := "".join(f"<#{channel}>\n" for channel in await db.LevelIgnoreChannel.ID.get_all(where={db.LevelIgnoreChannel.SERVER: interaction.guild.id}))):
            output_ignore_channels = "`In this server you can earn XP in all channels`"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            title = "Levels Overview",
            fields = [
                EmbedField(
                    "What are levels?",
                    "For every message you send you earn experience (xp). These xp points will make you level up. The more you chat, the more xp you earn and the higher your level gets. You can see your level by using `/levels info`.",
                    False
                ),
                EmbedField(
                    "Level-Roles:",
                    output_role_list,
                    False
                ),
                EmbedField(
                    "No XP Channels:",
                    output_ignore_channels,
                    False
                )
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsOverview(client))