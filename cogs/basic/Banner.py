import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Banner(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["banner"].name,
        Commands().data["avatar"].description,
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def banner(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["banner"].parameters["user"].name,
            Commands().data["banner"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command reposts anyone's banner in an embed"""

        user = user or interaction.user

        if not (user_banner := (await interaction.guild.fetch_member(user.id)).display_banner if interaction.guild else (await self.client.fetch_user(user.id)).banner):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"The user {user.mention} doesn't have a banner."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            image = user_banner.url,
            title = f"Banner of: `{user.display_name}`",
            title_url = user_banner.url
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Banner(client))