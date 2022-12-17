####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Avatar(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "avatar", description = "posts someone's avatar")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def avatar(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want the avatar from", required=False)):
        """This command reposts anyone's avatar in an embed"""
        
        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /avatar {member.id}")

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            image = member.display_avatar.url,
            title = f"Avatar of: `{member.display_name}`",
            title_url = member.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Avatar(client))