import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
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
            title = f"Levels information for `{member.display_name}` on `{interaction.guild.name}`",
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
    client.add_cog(LevelsInfo(client))