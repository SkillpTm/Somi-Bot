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
            required = False,
            choices = Lists().SOMICORD_RULES.keys()
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["rules"].parameters["channel"].name,
            Commands().data["rules"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
    ) -> None:
        """This command let's you post an embed for the specified or all rules"""

        channel = channel or interaction.channel

        await interaction.response.defer(ephemeral=True, with_message=True)

        # "0 All Rules" has a empty description, all other rules have a description
        if rule:
            embed = EmbedFunctions().builder(
                color = Lists().SOMICORD_RULES[rule][0],
                author = f"Rule: {rule}",
                author_icon = interaction.guild.icon.url,
                description = Lists().SOMICORD_RULES[rule][1],
                footer = Lists().SOMICORD_RULES[rule][2]
            )

            await channel.send(embed=embed) # type: ignore
            await interaction.send(embed=EmbedFunctions().get_success_message(f"Rule: `{rule}` sent in {channel.mention}"))
            return


        for key, val in Lists().SOMICORD_RULES.items():
            embed = EmbedFunctions().builder(
                color = val[0],
                author = f"Rule: {key}",
                author_icon = interaction.guild.icon.url,
                description = val[1],
                footer = val[2]
            )

            await channel.send(embed=embed) # type: ignore

        embed = EmbedFunctions().builder(
            color = 0xe97ead,
            image = Config().BAN_HAMMER_GIF,
            author = "Failing to follow the rules",
            author_icon = interaction.guild.icon.url,
            description = 'If you fail to follow any of these rules, or are deemed "unwelcome, because of your behaviour" the "case-by-case principle" will be used and your punishment will range from a warning to a ban.'
        )

        await channel.send(embed=embed) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_success_message(f"All rules sent in {channel.mention}"))



def setup(client: SomiBot) -> None:
    client.add_cog(Rules(client))