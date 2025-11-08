import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.utilities import SomiBot



class Userinfo(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "ui",
        description = "gives information about a user",
        name_localizations = {country_tag:"userinfo" for country_tag in nextcord.Locale}
    )
    async def userinfo(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want information about",
            required = False
        )
    ) -> None:
        """This command gives you infomration about a user"""

        await interaction.response.defer(with_message=True)

        user = user or interaction.user

        # empty server data, if left empty the coresponding fields will not be dispalyed
        booster, joined_time, status, top_role = "", "", "", ""

        # if the command was made in a guild also add data regarding the guild
        if interaction.guild:
            member = interaction.guild.get_member(user.id)

            status = str(member.status)
            top_role = member.top_role.mention
            booster = "Yes" if member.premium_since else "No"
            joined_time = f"<t:{int(time.mktime(member.joined_at.timetuple()))}>"

        embed = EmbedFunctions().builder(
            color = user.color,
            thumbnail = user.display_avatar.url,
            title = f"User Information: `{user.display_name}`",
            fields = [
                [
                    "ID:",
                    user.id,
                    False
                ],

                [
                    "Username:",
                    user.name,
                    True
                ],

                [
                    "Display Name:",
                    user.display_name,
                    True
                ],

                [
                    "Status:",
                    status,
                    True
                ],

                [
                    "Top role:",
                    top_role,
                    True
                ],

                [
                    "Booster:",
                    booster,
                    True
                ],

                [
                    "Joined Discord:",
                    f"<t:{int(time.mktime(user.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Joined Server:",
                    joined_time,
                    True
                ],

                [
                    "Public Flags:",
                    ", ".join(flag.name for flag in user.public_flags.all()),
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Userinfo(client))