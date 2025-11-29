import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class LevelsInfo(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.levels.subcommand(
        Commands().data["levels info"].alias,
        Commands().data["levels info"].description,
        name_localizations = {country_tag: Commands().data["levels info"].name for country_tag in nextcord.Locale}
    )
    async def levels_info(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["levels info"].parameters["member"].name,
            Commands().data["levels info"].parameters["member"].description,
            required = False
        )
    ) -> None:
        """Displays any users level, rank and level progression, with a progession bar"""

        member = member or interaction.guild.get_member(interaction.user.id)

        if not (total_xp := int(await db.Level.XP.get({db.Level.SERVER: interaction.guild.id, db.Level.USER: interaction.user.id}) or 0)):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{member.mention} hasn't earned any XP yet."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        user_level = db.Level._.get_level(total_xp)
        next_level_xp = (user_level+1) * 200
        xp_progress_to_next_level = next_level_xp - db.Level._.get_xp_until_next_level(total_xp, user_level)
        output_percentage = int((float(xp_progress_to_next_level) / float(next_level_xp)) * 100)

        # calculate a 20 segment progress bar with the percentage of xp to the next level
        percent = 20 * (float(xp_progress_to_next_level) / float(next_level_xp))
        percent_bar = "[" + "█" * int(percent) + " -" * (20 - int(percent)) + "]"

        footer, footer_time = self.client.joined_time_footer(interaction)

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            thumbnail = member.display_avatar.url,
            title = f"Levels information for `{member.display_name}` on `{interaction.guild.name}`",
            footer = footer,
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = footer_time,
            fields = [
                EmbedField(
                    "Level:",
                    f"`{user_level}`",
                    True
                ),
                EmbedField(
                    "Rank:",
                    f"`{f"{await db.Level._.get_user_rank({db.Level.SERVER: interaction.guild.id, db.Level.USER: interaction.user.id}):,}/{member.guild.member_count:,}"}`",
                    True
                ),
                EmbedField(
                    "Total XP:",
                    f"`{f"{total_xp:,}"}`",
                    True
                ),
                EmbedField(
                    "Level Progress:",
                    f"{percent_bar}\n{f"{xp_progress_to_next_level:,}"}/{f"{next_level_xp:,}"} ({output_percentage}%)",
                    False
                )
            ]
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsInfo(client))