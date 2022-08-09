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



class kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###kick###########################################################
        
    @nextcord.slash_command(name="kick", description="[MOD] kicks a member")
    @application_checks.has_any_role(MODERATOR_ID)
    async def kick(self,
                   interaction: Interaction,
                   *,
                   member: nextcord.Member = SlashOption(description="Member to be kicked", required=True),
                   reason: str = SlashOption(description="Reason for the kick", required=False, min_length=2, max_length=1000)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /kick {member} {reason}")

        if await is_member_skillp(interaction, member, source = "kick"):
            return
        if await is_member_themself(interaction, member, source = "kick"):
            return
        
        if reason != None:
            await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nFor the reason:\n`{reason}`\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")
        else:
            await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nThere was no provided reason.\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")

        await member.kick(reason=reason)

        if reason != None:
            await interaction.response.send_message(f"Succesfully kicked {member.mention} because: `{reason}`.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Succesfully kicked {member.mention}.", ephemeral=True)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = Color.orange(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "/kick:",
                              field_one_value = f"{interaction.user.mention} kicked: {member.mention}",
                              field_one_inline = False,

                              field_two_name = "Reason:",
                              field_two_value = reason,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "kick")

    @kick.error
    async def kick_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

def setup(client):
    client.add_cog(kick(client))