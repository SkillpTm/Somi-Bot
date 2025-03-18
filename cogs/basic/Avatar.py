import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Avatar(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="avatar", description="posts someone's avatar")
    async def avatar(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description = "the user you want the avatar from",
            required = False
        )
    ) -> None:
        """This command reposts anyone's avatar in an embed"""
        
        if not user:
            user = interaction.user

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/avatar",
            {"user": str(user.id)}
        ))

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            image = user.display_avatar.url,
            title = f"Avatar of: `{user.display_name}`",
            title_url = user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Avatar(client))