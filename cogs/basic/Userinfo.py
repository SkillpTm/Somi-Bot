####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import time

####################################################################################################

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Userinfo(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "ui", description = "gives information about a user", name_localizations = {country_tag:"userinfo" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def userinfo(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description="the user you want information about",
            required=False
        )
    ) -> None:
        """This command gives you infomration about a user"""

        if not user:
            user = interaction.user

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/userinfo",
            {"user": str(user.id)}
        ))

        await interaction.response.defer(with_message=True)

        # empty server data, if left empty the coresponding fields will not be dispalyed
        booster, joined_time, status, top_role = "", "", "", ""

        # if the command was made in a guild also add data regarding the guild
        if interaction.guild:
            member = interaction.guild.get_member(user.id)

            status = str(member.status)
            top_role = member.top_role.mention

            if member.premium_since:
                booster = "Yes"
            else:
                booster = "No"

            joined_time = f"<t:{int(time.mktime(member.joined_at.timetuple()))}>"

            # special case due to there not having been a fail save on /kick while testing, simply sets the correct join time
            if member.id == self.client.owner_id and member.guild.id == self.client.SOMICORD_ID:
                joined_time = f"<t:{self.client.SKILLP_JOINED_SOMICORD_TIME}>"

        embed = EmbedFunctions().builder(
            color = member.color,
            thumbnail = member.display_avatar.url,
            title = f"User Information: `{member.display_name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "ID:",
                    user.id,
                    False
                ],

                [
                    "Username:",
                    user.global_name,
                    True
                ],

                [
                    "Display Name:",
                    user.display_name,
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(user.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Public Flags:",
                    ", ".join(user.public_flags.all()),
                    True
                ]

                [
                    "Top role:",
                    top_role,
                    True
                ],

                [
                    "Status:",
                    status,
                    True
                ],

                [
                    "Joined at:",
                    joined_time,
                    True
                ],

                [
                    "Booster:",
                    booster,
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Userinfo(client))