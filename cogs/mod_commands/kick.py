###package#import###############################################################################

import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, is_member_skillp, is_member_themself
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID



class kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###kick###########################################################
        
    @nextcord.slash_command(name="kick", description="kicks a member")
    @application_checks.has_any_role(MODERATOR_ID)
    async def kick(self,
                   interaction: Interaction,
                   *,
                   member: nextcord.Member = SlashOption(description="Member to be kicked", required=True),
                   reason: str = SlashOption(description="Reason for the kick", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /kick {member} {reason}")

        if await is_member_skillp(interaction, member, source = "kick"):
            return
        if await is_member_themself(interaction, member, source = "kick"):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        await member.kick(reason=reason)

        if reason != None:
            await interaction.response.send_message(f"Succesfully kicked {member.mention} because: {reason}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Succesfully kicked {member.mention}", ephemeral=True)

        embed = Embed(colour=Color.orange())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        if reason != None:
            embed.add_field(name = "/kick:", value = f"{interaction.user.mention} kicked: {member.mention}\nBecause: {reason}", inline = True)
        else:
            embed.add_field(name = "/kick:", value = f"{interaction.user.mention} kicked: {member.mention}", inline = True)
        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "kick")

    @kick.error
    async def kick_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(kick(client))