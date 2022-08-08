###package#import###############################################################################

import nextcord
from nextcord import Color, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, is_member_skillp, is_member_themself, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, SKILLP_ID



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

        if reason != None:
            await member.send(f"You have been __**banned**__ from `{member.guild.name}`\nFor the reason:\n`{reason[:3800]}`\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")
        else:
            await member.send(f"You have been __**banned**__ from `{member.guild.name}`\nThere was no provided reason.\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")

        await member.ban(reason=reason)

        if reason != None:
            await interaction.response.send_message(f"Succesfully banned <@{member.id}> because: `{reason[:4000]}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"Succesfully banned <@{member.id}>", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = Color.red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "/ban:",
                              field_one_value = f"{interaction.user.mention} banned: {member.mention}",
                              field_one_inline = False,

                              field_two_name = "Reason:",
                              field_two_value = reason,
                              field_two_inline = False)

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
                    member_id = SlashOption(description="User ID of user to be unbanned", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /unban {member_id}")

        try:
            user = await self.client.fetch_user(member_id)
        except:
            await interaction.response.send_message(f"`{member_id[:4000]}` isn't a discord user", ephemeral=True)
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        try:
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user.mention} has been unbanned", ephemeral=True)
        except:
            await interaction.response.send_message(f"{user.mention} wasn't banned", ephemeral=True)
            return

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = Color.green(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "/unban:",
                              field_one_value = f"{interaction.user.mention} unbanned: {user.mention}",
                              field_one_inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "unban")

    @unban.error
    async def unban_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(ban(client))