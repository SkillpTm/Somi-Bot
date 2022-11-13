###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR



class vcaccess(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###vcaccess###########################################################

    @nextcord.slash_command(name="vcaccess", description="[MOD] grants/takes away a user's access to the voice channels (ignoring level roles)")
    @application_checks.has_any_role(MODERATOR_ID)
    async def vcaccess(self,
                  interaction: Interaction,
                  *,
                  member: nextcord.Member = SlashOption(description="member to be granted access/take access away", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /vcaccess {member}")

        for channel in interaction.guild.voice_channels:
            print(channel.permissions_for(member).value)
            if not channel.permissions_for(member).value == 418863451712: #418863451712 = if the user already has those permissions on that channel
                await channel.set_permissions(member, connect = True, speak = True, stream = True, use_voice_activation = True)
                permissions_added = True
                response = f"{member.mention} now has access to all voice channels!"

            else:
                await channel.set_permissions(member, connect = False, speak = False, stream = False, use_voice_activation = False)
                permissions_added = False
                response = f"{member.mention} now lost access to all voice channels"

        await interaction.response.send_message(response, ephemeral=True)

        if permissions_added:
            action_text = f"{interaction.user.mention} gave {member.mention} access to all voice channels."
        else:
            action_text = f"{interaction.user.mention} took access from all voice channels of {member.mention} away."

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = MOD_COLOR,
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/vcaccess:",
                              field_one_value = action_text,
                              field_one_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "vcaccess")

    @vcaccess.error
    async def error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)


def setup(client):
    client.add_cog(vcaccess(client))