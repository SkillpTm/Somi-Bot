####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import time

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Userinfo(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "ui", description = "gives information about a user", name_localizations = {country_tag:"userinfo" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def userinfo(self,
                       interaction: nextcord.Interaction,
                       *,
                       member: nextcord.Member = nextcord.SlashOption(description="the user you want information about", required=False)):
        """This command gives you infomration about a user"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /userinfo {member.id}")

        await interaction.response.defer(with_message=True)

        if member.id == self.client.owner_id and member.guild.id == self.client.SOMICORD_ID:
            joined_time = self.client.SKILLP_JOINED_SOMICORD_TIME
        else:
            joined_time = int(time.mktime(member.joined_at.timetuple()))

        embed = EmbedFunctions().builder(
            color = member.color,
            thumbnail = member.display_avatar.url,
            title = f"User Information: `{member.display_name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "ID:",
                    member.id,
                    False
                ],

                [
                    "Name:",
                    member.name,
                    True
                ],

                [
                    "Top role:",
                    member.top_role.mention,
                    True
                ],

                [
                    "Status:",
                    member.status,
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
                    True
                ],

                [
                    "Joined at:",
                    f"<t:{joined_time}>",
                    True
                ],

                [
                    "Boosted:",
                    bool(member.premium_since),
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Userinfo(client))