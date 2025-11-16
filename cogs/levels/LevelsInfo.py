import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class LevelsInfo(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(
        Commands().data["levels info"].alias,
        Commands().data["levels info"].description,
        name_localizations = {country_tag: Commands().data["levels info"].name for country_tag in nextcord.Locale}
    )
    async def levels_info(
        self,
        interaction: nextcord.Interaction,
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["levels info"].parameters["member"].name,
            Commands().data["levels info"].parameters["member"].description,
            required = False
        )
    ) -> None:
        """Displays any users level, rank and level progression, with a progession bar"""

        member = member or interaction.guild.get_member(interaction.user.id)

        if not (total_xp := await db.Level.XP.get({db.Level.SERVER: interaction.guild.id, db.Level.USER: interaction.user.id})):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{member.mention} hasn't earned any XP yet."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        user_level = db.Level._.get_level(total_xp)
        next_level_xp = (user_level+1) * 200
        xp_progress_to_next_level = next_level_xp - db.Level._.get_xp_until_next_level(total_xp, user_level)
        output_percentage = int((float(xp_progress_to_next_level) / float(next_level_xp)) * 100)

        # calculate a 20 segment progress bar with the percentage of xp to the next level
        percent = 20 * (float(xp_progress_to_next_level) / float(next_level_xp))
        percent_bar = "[" + "█" * int(percent) + " -" * (20 - int(percent)) + "]"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = member.display_avatar.url,
            title = f"Levels information for `{member.display_name}` on `{interaction.guild.name}`",
            fields = [
                [
                    "Level:",
                    f"`{user_level}`",
                    True
                ],

                [
                    "Rank:",
                    f"`{f"{await db.Level._.get_user_rank({db.Level.SERVER: interaction.guild.id, db.Level.USER: interaction.user.id}):,}/{member.guild.member_count:,}"}`",
                    True
                ],

                [
                    "Total XP:",
                    f"`{f"{total_xp:,}"}`",
                    True
                ],

                [
                    "Level Progress:",
                    f"{percent_bar}\n{f"{xp_progress_to_next_level:,}"}/{f"{next_level_xp:,}"} ({output_percentage}%)",
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsInfo(client))