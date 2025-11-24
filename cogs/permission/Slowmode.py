import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.managers import Commands, Lists
from lib.helpers import EmbedField, EmbedFunctions
from lib.modules import SomiBot



class Slowmode(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["slowmode"].name,
        Commands().data["slowmode"].description,
        default_member_permissions = nextcord.Permissions(manage_channels=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def slowmode(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        delay: int = nextcord.SlashOption(
            Commands().data["slowmode"].parameters["delay"].name,
            Commands().data["slowmode"].parameters["delay"].description,
            required = True,
            min_value = 0,
            max_value = 21600 # 6 hours in seconds
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["slowmode"].parameters["channel"].name,
            Commands().data["slowmode"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
    ) -> None:
        """This command allows a user to set a slowmode in a channel."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        channel = channel or interaction.channel

        await channel.edit(slowmode_delay=delay)

        if delay:
            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Activated slowmode in {channel.mention} with a delay of `{delay}` seconds."), ephemeral=True)
            mod_action = f"{interaction.user.mention} activated slowmode in {channel.mention} with a delay of `{delay} seconds`"
        else:
            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Deactivated slowmode in {channel.mention}."), ephemeral=True)
            mod_action = f"{interaction.user.mention} deactivated slowmode in {channel.mention}"

        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return


        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["slowmode"].name}:",
                    mod_action,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(Slowmode(client))