import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Config
from lib.utilities import SomiBot



class LevelsRank(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(name="rank", description="shows your rank and level on this server")
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

        member = member or interaction.guild.get_member(interaction.user.id)

        await interaction.response.defer(with_message=True)

        user_level, xp_until_next_level = await (await DBHandler(self.client.database, server_id=interaction.guild.id, user_id=interaction.user.id).level()).get_level_and_xp_until_next()
        next_level_xp = (user_level+1) * 200
        xp_progress_to_next_level = next_level_xp - xp_until_next_level
        output_percentage = int((float(xp_progress_to_next_level) / float(next_level_xp)) * 100)

        # calculate a 20 segment progress bar with the percentage of xp to the next level
        percent = 20 * (float(xp_progress_to_next_level) / float(next_level_xp))
        percent_bar = "[" + "█" * int(percent) + " -" * (20 - int(percent)) + "]"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = member.display_avatar.url,
            title = f"Rank for `{member.display_name}` on `{interaction.guild.name}`",
            fields = [
                [
                    "Level:",
                    f"`{user_level}`",
                    True
                ],

                [
                    "Rank:",
                    f"`{f"{await (await DBHandler(self.client.database, server_id=interaction.guild.id, user_id=interaction.user.id).level()).get_rank():,}"}`",
                    True
                ],

                [
                    "Total XP:",
                    f"`{f"{await (await DBHandler(self.client.database, server_id=interaction.guild.id, user_id=interaction.user.id).level()).get_total_xp():,}"}`",
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
    client.add_cog(LevelsRank(client))