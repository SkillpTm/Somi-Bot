import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot



class Rules(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["rules"].name,
        Commands().data["rules"].description,
        guild_ids = [Config().MODMAIL_SERVER_ID, Config().SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def rules(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        rule: str = nextcord.SlashOption(
            Commands().data["rules"].parameters["rule"].name,
            Commands().data["rules"].parameters["rule"].description,
            required = True,
            choices = [
                "1 NSFW Content",
                "2 Doxxing",
                "3 Cursing",
                "4 Language",
                "5 Discrimination",
                "6 Channel Use",
                "7 Unboxing Spoiler Tags",
                "8 Spam",
                "9 Negativity",
                "10 Selfpromotion",
                "11 Relationships"
            ]
        )
    ) -> None:
        """This command let's you post an embed for the specified rule."""

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.brand_red(),
            author = f"Rule {rule}",
            author_icon = interaction.guild.icon.url, 
            description = Lists().SOMICORD_RULES[rule][0],
            footer = Lists().SOMICORD_RULES[rule][1]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Rules(client))