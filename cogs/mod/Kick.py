####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import AuditLogChannelDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Kick(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################
        
    @nextcord.slash_command(name="kick", description="kicks a member", default_member_permissions = nextcord.Permissions(kick_members=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def kick(self,
                   interaction: nextcord.Interaction,
                   *,
                   member: nextcord.Member = nextcord.SlashOption(description="Member to be kicked", required=True),
                   reason: str = nextcord.SlashOption(description="Reason for the kick", required=False, min_length=2, max_length=1000)):
        """This command kicks a member with a reason."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /kick {member.id}\n{reason}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.followup.send(embed=EmbedFunctions().error("You can't ban yourself!"), ephemeral=True)
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.user.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only kick a member, if your current top-role is above their current top-role!"), ephemeral=True)
            return
        
        try:
            if reason != None:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nFor the reason:\n`{reason}`")
            else:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nThere was no provided reason.")
        except:
            pass

        await member.kick(reason=reason)

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully kicked {member.mention}."), ephemeral=True)


        audit_log_id = AuditLogChannelDB().get(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/kick:",
                    f"{interaction.user.mention} kicked: {member.mention}",
                    False
                ],

                [
                    "Reason:",
                    reason,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Kick(client))