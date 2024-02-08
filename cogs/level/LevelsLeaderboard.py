####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import LevelsDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class LevelsLeaderboard(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import levels

    ####################################################################################################

    @levels.subcommand(name = "top", description = "shows the top users by level of this server", name_localizations = {country_tag:"leaderboard" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def levels_leaderboard(self,
                                 interaction: nextcord.Interaction):
        """Displays the top 10 (or less, if there isn't 10 users in the levels table) users by XP"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /levels leaderboard")

        await interaction.response.defer(with_message=True)

        user_ids_and_levels = LevelsDB(interaction.guild.id).get_all_user_levels(10)
        output: str = ""

        for index, user in enumerate(user_ids_and_levels):
            try:
                member = interaction.guild.get_member(user[0])
            except:
                member = self.client.get_user(user[0])

            if isinstance(member, nextcord.Member):
                name = member.mention
            elif isinstance(member, nextcord.User):
                name = member.display_name
            else:
                name = "[Deleted User]"

            output += f"**{index+1}. {name}** - Level: __`{user[1]}`__\n"

        if interaction.guild.icon:
            server_icon_url = interaction.guild.icon
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



def setup(client: SomiBot):
    client.add_cog(LevelsLeaderboard(client))