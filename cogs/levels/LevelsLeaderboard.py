import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.utilities import SomiBot



class LevelsLeaderboard(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(
        Commands().data["levels leaderboard"].alias,
        Commands().data["levels leaderboard"].description,
        name_localizations = {country_tag: Commands().data["levels leaderboard"].name for country_tag in nextcord.Locale}
    )
    async def levels_leaderboard(self, interaction: nextcord.Interaction) -> None:
        """Displays the top 10 (or less, if there isn't 10 users in the levels table) users by XP"""

        await interaction.response.defer(with_message=True)

        output: str = ""

        for index, user_data in enumerate(await (await DBHandler(self.client.database, server_id=interaction.guild.id).level()).get_all_users_ranked(limit=10)):
            name = f"[Deleted User] - ({user_data[0]})" # default value for, if the user's account doesn't exit anymore

            # check if the user is still in the server
            if (member := interaction.guild.get_member(user_data[0])):
                name = member.mention
            # check if the user's account still exists
            elif not member and (user := self.client.get_user(user_data[0])):
                name = user.display_name

            output += f"**{index+1}. {name}** - Level: __`{user_data[1]}`__\n"

        server_icon_url = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = server_icon_url,
            title = f"`{interaction.guild.name}`: Top users by level",
            description = output
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsLeaderboard(client))