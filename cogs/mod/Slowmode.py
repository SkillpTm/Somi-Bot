####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import AuditLogChannelDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import TEXT_CHANNELS, SomiBot



class Slowmode(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################
        
    @nextcord.slash_command(name="slowmode", description="sets/unsets a slowmode in a channel", default_member_permissions = nextcord.Permissions(manage_channels=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def slowmode(self,
                       interaction: nextcord.Interaction,
                       *,
                       delay: int = nextcord.SlashOption(description="how long it takes until a user can send a message again in seconds. (To end slowmode input '0')", required=True, min_value = 0, max_value = 21600),
                       channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=TEXT_CHANNELS, description="the channel to activate slowmode in", required=False)):
        """This command allows a user to set a slowmode in a channel."""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /slowmode {delay} {channel.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        await channel.edit(slowmode_delay=delay)

        if not delay == 0:
            await interaction.followup.send(embed=EmbedFunctions().success(f"Activated slowmode in {channel.mention} with a delay of `{delay}` seconds."), ephemeral=True)
        else:
            await interaction.followup.send(embed=EmbedFunctions().success(f"Deactivated slowmode in {channel.mention}."), ephemeral=True)


        audit_log_id = AuditLogChannelDB().get(interaction.guild)

        if not audit_log_id:
            return

        if not delay == 0:
            mod_action = f"{interaction.user.mention} activated slowmode in {channel.mention} with a delay of `{delay} seconds`"
        else:
            mod_action = f"{interaction.user.mention} deactivated slowmode in {channel.mention}"

        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/slowmode:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Slowmode(client))