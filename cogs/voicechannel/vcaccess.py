###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, LEVELROLES, MOD_COLOR



class vcaccess(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###vcaccess###########################################################

    @nextcord.slash_command(name="vcaccess", description="Grants/takes away a user's access to the voice channels (ignoring level roles)")
    @application_checks.has_any_role(MODERATOR_ID)
    async def vcaccess(self,
                  interaction: Interaction,
                  *,
                  member: nextcord.Member = SlashOption(description="Member to be granted access/take access away", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /vcaccess {member}")

        for role_id in LEVELROLES:
            role = interaction.guild.get_role(int(role_id))
            if role in member.roles:
                await interaction.response.send_message(f"{member} already has access to the voice channels!", ephemeral=True)
                return

        for channel in interaction.guild.voice_channels:
            if not channel.permissions_for(member).value == 418863451712: #418863451712 = if the user already has those permissions on that channel
                await channel.set_permissions(member, connect = True, speak = True, stream = True, use_voice_activation = True)
                permissions_added = True
            else:
                await channel.set_permissions(member, connect = False, speak = False, stream = False, use_voice_activation = False)
                permissions_added = False

        await interaction.response.send_message(f"{member} now has access to all voice channels!", ephemeral=True)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        embed = Embed(colour=MOD_COLOR)
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)

        if permissions_added:
            embed.add_field(name = "/vcaccess:", value = f"{interaction.user.mention} gave {member.mention} access to all voice channels", inline = False)
        else:
            embed.add_field(name = "/vcaccess:", value = f"{interaction.user.mention} took access from all voice channels of {member.mention} away", inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "vcaccess")

    @vcaccess.error
    async def error(interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)


def setup(client):
    client.add_cog(vcaccess(client))