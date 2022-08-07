###package#import###############################################################################

import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands
from datetime import timedelta

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, is_member_skillp, is_member_themself, time_to_seconds
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID



class mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###mute###########################################################

    @nextcord.slash_command(name="mute", description="mutes a user")
    @application_checks.has_any_role(MODERATOR_ID)
    async def mute(self,
                   interaction: Interaction,
                   *,
                   member: nextcord.Member = SlashOption(description="The member to be muted", required=True),
                   time: str = SlashOption(description="The time to mute the member for (input: xd and/or xh and/or xm and/or xs) Example: 5d7h28s)", required=True),
                   reason: str = SlashOption(description="Reason for the mute", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /mute {member} {time} {reason}")

        if await is_member_skillp(interaction, member, source = "mute"):
            return
        if await is_member_themself(interaction, member, source = "mute"):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        total_seconds = time_to_seconds(time)

        if total_seconds == 0 or total_seconds > 2419200: #28d in seconds
            await interaction.response.send_message(f"`{time[:3900]}` is not a valid time period. Make sure to use the formating in the input description and that your time period is smaller than 28d.", ephemeral=True)
            return

        await member.edit(timeout=nextcord.utils.utcnow()+timedelta(seconds=total_seconds))
        if reason != None:
            await interaction.response.send_message(f"{member.mention} has been muted because: {reason}", ephemeral=True)
        else:
            await interaction.response.send_message(f"{member.mention} has been muted", ephemeral=True)

        embed = Embed(colour=Color.yellow())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/mute:", value = f"{interaction.user.mention} muted: {member.mention} for: `{time}`", inline = True)

        if reason != None:
            embed.add_field(name = "Reason:", value = reason[:1000], inline = False)
        else:
            pass

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "mute")

    @mute.error
    async def mute_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

    ###unmute###########################################################

    @nextcord.slash_command(name="unmute", description="unmutes a user")
    @application_checks.has_any_role(MODERATOR_ID)
    async def unmute(self,
                     interaction: Interaction,
                     *,
                     member: nextcord.Member = SlashOption(description="Member to be unmuted", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /unmute {member}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        if member.communication_disabled_until != None:
            await member.edit(timeout=None)
            await interaction.response.send_message(f"{member.mention} has been unmuted", ephemeral=True)
        else:
            await interaction.response.send_message(f"{member.mention} wasn't muted", ephemeral=True)
            return

        embed = Embed(colour=Color.green())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/unmute:", value = f"{interaction.user.mention} unmuted: {member.mention}", inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "unmute")

    @unmute.error
    async def unmute_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(mute(client))