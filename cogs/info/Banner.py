####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Banner(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "banner", description = "posts someone's banner")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def banner(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want the banner from", required=False)):
        """This command reposts anyone's banner in an embed"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /banner {member.id}")

        user = await self.client.fetch_user(member.id)

        if not hasattr(user.banner, "url"):
            await interaction.response.send_message(embed=EmbedFunctions().error(f"The user {member.mention} doesn't have a banner."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            image = user.banner.url,
            title = f"Banner of: `{member.display_name}`",
            title_url = user.banner.url,
            footer = "DEFAULT_KST_FOOTER"
        )
        
        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Banner(client))