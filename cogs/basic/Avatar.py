import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.utilities import SomiBot



class Avatar(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(Commands().data["avatar"].name, Commands().data["avatar"].description)
    async def avatar(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["avatar"].parameters["user"].name,
            Commands().data["avatar"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command reposts anyone's avatar in an embed"""

        await interaction.response.defer(with_message=True)

        user = user or interaction.user

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            image = user.display_avatar.url,
            title = f"Avatar of: `{user.display_name}`",
            title_url = user.display_avatar.url
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Avatar(client))