import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Banner(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="banner", description="posts someone's banner")
    async def banner(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description="the user you want the banner from",
            required=False
        )
    ) -> None:
        """This command reposts anyone's banner in an embed"""

        if not user:
            user = interaction.user

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/banner",
            {"user": str(user.id)}
        ))

        if interaction.guild:
            user_banner_url = (await interaction.guild.fetch_member(user.id)).display_banner.url
        else:
            user_banner_url = (await self.client.fetch_user(user.id)).banner.url


        if not user_banner_url:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"The user {user.mention} doesn't have a banner."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            image = user_banner_url,
            title = f"Banner of: `{user.display_name}`",
            title_url = user_banner_url,
            footer = "DEFAULT_KST_FOOTER"
        )
        
        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Banner(client))