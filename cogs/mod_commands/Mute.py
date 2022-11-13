###package#import###############################################################################

import datetime
import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, is_member_skillp, is_member_themself, time_to_seconds, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID



class Mute(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###mute###########################################################

    @nextcord.slash_command(name="mute", description="[MOD] mutes a user")
    @nextcord.ext.application_checks.has_permissions(mute_members=True)
    async def mute(self,
                   interaction: nextcord.Interaction,
                   *,
                   member: nextcord.Member = nextcord.SlashOption(description="the member to be muted", required=True),
                   time: str = nextcord.SlashOption(description="the time to mute the member for (input: xy | xw |xd | xh | xm | xs) example: 5d7h28s)", required=True, min_length=2, max_length=30),
                   reason: str = nextcord.SlashOption(description="reason for the mute", required=False, min_length=2, max_length=1000)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /mute {member} {time} {reason}")

        if await is_member_skillp(interaction, member, source = "mute"):
            return
        if await is_member_themself(interaction, member, source = "mute"):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        total_seconds = time_to_seconds(time)

        if total_seconds == 0 or total_seconds > 2419200: #28d in seconds
            await interaction.response.send_message(f"`{time}` is not a valid time period. Make sure to use the formating in the input description and that your time period is smaller than 28 days.", ephemeral=True)
            return

        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=total_seconds))

        await interaction.response.send_message(f"Succesfully muted {member.mention}.", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.yellow(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/mute:",
                              field_one_value = f"{interaction.user.mention} muted: {member.mention} for: `{time}`",
                              field_one_inline = False,

                              field_two_name = "Reason:",
                              field_two_value = reason,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "mute")

    @mute.error
    async def mute_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

    ###unmute###########################################################

    @nextcord.slash_command(name="unmute", description="[MOD] unmutes a user")
    @nextcord.ext.application_checks.has_permissions(mute_members=True)
    async def unmute(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="member to be unmuted", required=True)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /unmute {member}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        if member.communication_disabled_until == None:
            await interaction.response.send_message(f"{member.mention} wasn't muted", ephemeral=True)
            return

        await member.edit(timeout=None)
        await interaction.response.send_message(f"{member.mention} has been unmuted", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.green(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/unmute:",
                              field_one_value = f"{interaction.user.mention} unmuted: {member.mention}",
                              field_one_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "unmute")

    @unmute.error
    async def unmute_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Mute(client))