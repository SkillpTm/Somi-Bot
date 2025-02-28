import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import LevelsDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class LevelsRank(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import levels

    ####################################################################################################

    @levels.subcommand(name = "rank", description = "shows your rank and level on this server")
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def levels_rank(
        self,
        interaction: nextcord.Interaction,
        *,
        member: nextcord.Member = nextcord.SlashOption(
            description = "the member you want to see the rank of",
            required = False
        )
    ) -> None:
        """Displays any users level, rank and level progression, with a progession bar"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/levels rank",
            {"member": str(member.id)}
        ))

        await interaction.response.defer(with_message=True)

        user_level, xp_until_next_level = LevelsDB(interaction.guild.id).get_level(member.id)
        next_level_xp = (user_level-1) * 200 + 300
        xp_progress_to_next_level = next_level_xp - xp_until_next_level
        
        # calculate a 20 segment progress bar with the percentage of xp to the next level
        percent = 20 * (float(xp_progress_to_next_level) / float(next_level_xp))
        percent_bar = "[" + "█" * int(percent) + " -" * (20 - int(percent)) + "]"

        output_percentage = int((float(xp_progress_to_next_level) / float(next_level_xp)) * 100)

        # a user with level 0 hasn't send a message yet, so we set some values manually
        if user_level == 0:
            xp_progress_to_next_level = 0
            next_level_xp = 0
            output_percentage = 100

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            thumbnail = member.display_avatar.url,
            title = f"Rank for `{member.display_name}` on `{interaction.guild.name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Level:",
                    f"`{user_level}`",
                    True
                ],

                [
                    "Rank:",
                    f"`{LevelsDB(interaction.guild.id).get_rank(member.id)}`",
                    True
                ],

                [
                    "Level Progress:",
                    f"{percent_bar}\n{xp_progress_to_next_level}/{next_level_xp} ({output_percentage}%)",
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsRank(client))