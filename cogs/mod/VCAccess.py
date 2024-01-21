####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class VCAccess(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="vc-access", description="grants/takes away a user's access to the voice-channels", default_member_permissions = nextcord.Permissions(manage_channels=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def vcaccess(self,
                       interaction: nextcord.Interaction,
                       *,
                       action: str = nextcord.SlashOption(description="which action do you want to take", required=True, choices=["Allow", "Forbid"]),
                       member: nextcord.Member = nextcord.SlashOption(description="member to be granted access/take access away", required=True)):
        """This command can restirct or grant access to all voice-channels in a guild."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /vc-access {action} {member.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.guild.voice_channels == []:
                await interaction.followup.send(embed=EmbedFunctions().error("This server doesn't have any voice-channels."), ephemeral=True)
                return

        if action == "Allow":
            for channel in interaction.guild.voice_channels:
                await channel.set_permissions(member, connect = True, speak = True, stream = True, use_voice_activation = True)

            await interaction.followup.send(embed=EmbedFunctions().success(f"{member.mention} now has access to all voice-channels."), ephemeral=True)

        elif action == "Forbid":
            for channel in interaction.guild.voice_channels:
                await channel.set_permissions(member, connect = False, speak = False, stream = False, use_voice_activation = False)

            await interaction.followup.send(embed=EmbedFunctions().success(f"{member.mention} now has lost access to all voice-channels"), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        if action == "Allow":
            mod_action = f"{interaction.user.mention} gave {member.mention} access to all voice-channels."
        elif action == "Forbid":
            mod_action = f"{interaction.user.mention} took access to all voice-channels from {member.mention} away."

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/vc-access:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(VCAccess(client))