import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LevelsLeaderboard(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(name = "top", description = "shows the top users by level of this server", name_localizations = {country_tag:"leaderboard" for country_tag in nextcord.Locale})
    async def levels_leaderboard(self, interaction: nextcord.Interaction) -> None:
        """Displays the top 10 (or less, if there isn't 10 users in the levels table) users by XP"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/levels leaderboard"))

        await interaction.response.defer(with_message=True)

        user_ids_and_levels = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).level()).get_all_users_ranked(limit=10)
        output: str = ""

        for index, user_data in enumerate(user_ids_and_levels):
            member = interaction.guild.get_member(user_data[0])
            user = self.client.get_user(user_data[0])
            name = f"[Deleted User] - ({user_data[0]})" # default value for, if the user's account doesn't exit anymore

            # check if the user is still in the server
            if member:
                name = member.mention
            # check if the user's account still exists
            elif not member and user:
                name = user.display_name

            output += f"**{index+1}. {name}** - Level: __`{user_data[1]}`__\n"

        if interaction.guild.icon:
            server_icon_url = interaction.guild.icon.url
        else:
            server_icon_url = self.client.DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            thumbnail = server_icon_url,
            title = f"`{interaction.guild.name}`: Top users by level",
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsLeaderboard(client))