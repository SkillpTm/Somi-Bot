import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import pytz
import time as unix_time

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Mute(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="mute", description="mutes a member", default_member_permissions = nextcord.Permissions(mute_members=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def mute(self,
                   interaction: nextcord.Interaction,
                   *,
                   member: nextcord.Member = nextcord.SlashOption(description="the member to be muted", required=True),
                   time: str = nextcord.SlashOption(description="the time to mute the member for (input: xy | xw |xd | xh | xm | xs) example: 5d7h28s)", required=True, min_length=2, max_length=50),
                   reason: str = nextcord.SlashOption(description="reason for the mute", required=False, min_length=2, max_length=1000)):
        """This command mutes a member, with time and reason, if their current top-role is below your current top-role."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /mute {member.id} {time}\n{reason}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.followup.send(embed=EmbedFunctions().error("You can't mute yourself!"), ephemeral=True)
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.user.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only mute a member, if your current top-role is above their current top-role!"), ephemeral=True)
            return

        total_seconds = Get().seconds_from_time(time)

        if total_seconds == 0 or total_seconds > 2419200: #28d in seconds
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{time}` is not a valid time period. Make sure to use the formating in the input description and that your time period is smaller than 28 days."), ephemeral=True)
            return

        await member.edit(timeout=datetime.datetime.now(pytz.timezone('UTC'))+datetime.timedelta(seconds=total_seconds))

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully muted {member.mention}."), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/mute:",
                    f"{interaction.user.mention} muted: {member.mention} for: `{time}` (that's until: <t:{int(unix_time.time()) + total_seconds}:F>)",
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

    ####################################################################################################

    @nextcord.slash_command(name="unmute", description="unmutes a member", default_member_permissions = nextcord.Permissions(mute_members=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def unmute(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="member to be unmuted", required=True)):
        """This command unmutes a member, if they were muted."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /unmute {member.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if member.communication_disabled_until == None:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{member.mention} wasn't muted."), ephemeral=True)
            return

        await member.edit(timeout=None)

        await interaction.followup.send(embed=EmbedFunctions().success(f"{member.mention} has been unmuted"), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/unmute:",
                    f"{interaction.user.mention} unmuted: {member.mention}",
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Mute(client))