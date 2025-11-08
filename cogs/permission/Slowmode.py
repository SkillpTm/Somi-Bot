import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.utilities import Lists, SomiBot



class Slowmode(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "slowmode",
        description = "set/resets a slowmode in a channel",
        default_member_permissions = nextcord.Permissions(manage_channels=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def slowmode(
        self,
        interaction: nextcord.Interaction,
        *,
        delay: int = nextcord.SlashOption(
            description = "how long it takes until a user can send a message again in seconds. (To end slowmode input '0')",
            required = True,
            min_value = 0,
            max_value = 21600 # 6 hours in seconds
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            channel_types = Lists.TEXT_CHANNELS,
            description = "the channel to activate slowmode in",
            required = False
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

        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return


        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/slowmode:",
                    mod_action,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Slowmode(client))