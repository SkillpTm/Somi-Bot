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



class ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###ban###########################################################
        
    @nextcord.slash_command(name="ban", description="bans a member")
    @application_checks.has_any_role(MODERATOR_ID)
    async def ban(self,
                  interaction: Interaction,
                  *,
                  member: nextcord.Member = SlashOption(description="Member to be banned", required=True),
                  reason: str = SlashOption(description="Reason for the ban", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /ban {member}\nReason: {reason}")

        if await is_member_skillp(interaction, member, source = "ban"):
            return
        if await is_member_themself(interaction, member, source = "ban"):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        await member.ban(reason=reason)

        if reason != None:
            await interaction.response.send_message(f"Succesfully banned <@{member.id}> because: {reason}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Succesfully banned <@{member.id}>", ephemeral=True)

        embed = Embed(colour=Color.red())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)

        if reason != None:
            embed.add_field(name = "/ban:", value = f"{interaction.user.mention} banned: {member.mention}", inline = False)
            embed.add_field(name = "Reason:", value = reason, inline = False)
        else:
            embed.add_field(name = "/ban:", value = f"{interaction.user.mention} banned: {member.mention}", inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "ban")

    @ban.error
    async def ban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

    ###unban###########################################################

    @nextcord.slash_command(name="unban", description="unbans a user")
    @application_checks.has_any_role(MODERATOR_ID)
    async def unban(self,
                    interaction: Interaction,
                    *,
                    member_id: int = SlashOption(description="User ID of user to be unbanned", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /unban {member_id}")

        try:
            member = await self.client.fetch_user(member_id)
        except:
            await interaction.response.send_message(f"`{member_id[:4000]}` isn't a discord user", ephemeral=True)
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        try:
            await interaction.guild.unban(member)
            await interaction.response.send_message(f"{member.mention} has been unbanned", ephemeral=True)
        except:
            await interaction.response.send_message(f"{member.mention} wasn't banned", ephemeral=True)
            return

        embed = Embed(colour=Color.green())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/unban:", value = f"{interaction.user.mention} unbanned: {member.mention}", inline = True)
        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "unban")

    @unban.error
    async def unban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(ban(client))