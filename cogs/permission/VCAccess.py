import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class VCAccess(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "vc-access",
        description = "grants/takes away a user's access to the voice-channels",
        default_member_permissions = nextcord.Permissions(manage_channels=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def vcaccess(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Allow", "Forbid"]
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description = "member to be granted access/take access away",
            required = True
        )
    ) -> None:
        """This command can restirct or grant access to all voice-channels in a guild."""

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/slowmode",
            {"action": action, "member": (member.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not interaction.guild.voice_channels:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("This server doesn't have any voice-channels."), ephemeral=True)
            return

        if action == "Allow":
            for channel in interaction.guild.voice_channels:
                await channel.set_permissions(member, connect = True, speak = True, stream = True, use_voice_activation = True)

            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{member.mention} now has access to all voice-channels."), ephemeral=True)
            # used in the audit log embed later
            mod_action = f"{interaction.user.mention} gave {member.mention} access to all voice-channels."

        elif action == "Forbid":
            for channel in interaction.guild.voice_channels:
                await channel.set_permissions(member, connect = False, speak = False, stream = False, use_voice_activation = False)

            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{member.mention} now has lost access to all voice-channels"), ephemeral=True)
            # used in the audit log embed later
            mod_action = f"{interaction.user.mention} took access to all voice-channels from {member.mention} away."

        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = self.client.config.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/vc-access:",
                    mod_action,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(VCAccess(client))