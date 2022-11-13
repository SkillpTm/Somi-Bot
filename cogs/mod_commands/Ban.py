###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, is_member_skillp, is_member_themself, embed_builder, string_search_to_list
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, SKILLP_ID



class Ban(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###ban###########################################################
        
    @nextcord.slash_command(name="ban", description="[MOD] bans a member")
    @nextcord.ext.application_checks.has_permissions(ban_members=True)
    async def ban(self,
                  interaction: nextcord.Interaction,
                  *,
                  member: nextcord.Member = nextcord.SlashOption(description="member to be banned", required=True),
                  delete_messages_hours: int = nextcord.SlashOption(description="the amount of days someone's messages will get deleted for (default=1)", required=False, min_value=0, max_value=168),
                  reason: str = nextcord.SlashOption(description="reason for the ban", required=False, min_length=2, max_length=1000)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /ban {member}\nReason: {reason}")

        if await is_member_skillp(interaction, member, source = "ban"):
            return
        if await is_member_themself(interaction, member, source = "ban"):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        try:
            if reason != None:
                await member.send(f"You have been __**banned**__ from `{member.guild.name}`\nFor the reason:\n`{reason}`\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")
            else:
                await member.send(f"You have been __**banned**__ from `{member.guild.name}`\nThere was no provided reason.\n\nIf you believe this was undeserved please message <@{SKILLP_ID}>\nCommunications with this bot will be closed, you won't be able to message me anymore!")
        except:
            pass

        if delete_messages_hours == None:
            delete_messages_hours = 1

        delete_messages_hours_in_seconds = delete_messages_hours * 60 * 60

        await interaction.guild.ban(user = member, reason = reason, delete_message_seconds = delete_messages_hours_in_seconds)

        await interaction.response.send_message(f"Succesfully banned <@{member.id}>", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/ban:",
                              field_one_value = f"{interaction.user.mention} banned: {member.mention} and deleted their messages for: `{delete_messages_hours} day(s)`",
                              field_one_inline = False,

                              field_two_name = "Reason:",
                              field_two_value = reason,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "ban")

    @ban.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

    ###unban###########################################################

    @nextcord.slash_command(name="unban", description="[MOD] unbans a user")
    @nextcord.ext.application_checks.has_permissions(ban_members=True)
    async def unban(self,
                    interaction: nextcord.Interaction,
                    *,
                    member_id: str = nextcord.SlashOption(description="user ID of the user to be unbanned", required=True, min_length=18, max_length=19)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /unban {member_id}")

        try:
            user = await self.client.fetch_user(member_id)
        except:
            await interaction.response.send_message(f"`{member_id}` isn't a valid discord user id.", ephemeral=True)
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        try:
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user.mention} has been unbanned!", ephemeral=True)
        except:
            await interaction.response.send_message(f"{user.mention} wasn't banned.", ephemeral=True)
            return

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.green(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/unban:",
                              field_one_value = f"{interaction.user.mention} unbanned: {user.mention}",
                              field_one_inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "unban")

    @unban.error
    async def unban_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

    @unban.on_autocomplete("member_id")
    async def autocomplete_unban(self,
                                 interaction: nextcord.Interaction,
                                 member_id: str):
        bans = await interaction.guild.bans(limit=25).flatten() #Discord max is 25
        bans_ids = []

        for ban in bans:
            bans_ids.append(ban.user.id)

        autocomplete_list = string_search_to_list(member_id, bans_ids)

        await interaction.response.send_autocomplete(autocomplete_list)



def setup(client):
    client.add_cog(Ban(client))