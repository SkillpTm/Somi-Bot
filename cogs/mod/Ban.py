import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Ban(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "ban",
        description = "bans a member",
        default_member_permissions = nextcord.Permissions(ban_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def ban(
        self,
        interaction: nextcord.Interaction,
        *,
        member: nextcord.Member = nextcord.SlashOption(
            description = "member to be banned",
            required = True
        ),
        delete_message_hours: int = nextcord.SlashOption(
            description = "the amount of hours someone's messages will get deleted for (default=1)",
            required = False,
            min_value = 0,
            max_value = 168
        ),
        reason: str = nextcord.SlashOption(
            description = "reason for the ban",
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command bans a member, while providing a delete message amount (in seconds) and giving a reason. It also protects from self-bans."""

        if not delete_message_hours:
            delete_message_hours = 1

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/ban",
            {"member": str(member.id), "delete_message_hours": str(delete_message_hours), "reason": reason}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.followup.send(embed=EmbedFunctions().error("You can't ban yourself!"), ephemeral=True)
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.user.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only ban a member, if your current top-role is above their current top-role!"), ephemeral=True)
            return

        try:
            if reason:
                await member.send(f"You have been __**banned**__ from `{interaction.guild.name}`\nFor the reason:\n`{reason}`")
            else:
                await member.send(f"You have been __**banned**__ from `{interaction.guild.name}`\nThere was no provided reason.")
        except:
            self.client.Loggers.action_warning(f"/ban send ~ User: {member.id} couldn't be notified, because their pms aren't open to the client")

        await interaction.guild.ban(user = member, reason = reason, delete_message_seconds = delete_message_hours * 60 * 60)

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully banned {member.mention}."), ephemeral=True)

    ####################################################################################################

    @nextcord.slash_command(
        name = "unban",
        description = "unbans a user",
        default_member_permissions = nextcord.Permissions(ban_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def unban(
        self,
        interaction: nextcord.Interaction,
        *,
        user_id: str = nextcord.SlashOption(
            description = "user ID of the user to be unbanned",
            required = True,
            min_length = 18,
            max_length = 19
        )
    ) -> None:
        """This command unbans a user, if that user exists and was banned."""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/unban",
            {"user_id": str(user_id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not user_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{user_id}` isn't a valid discord user id."), ephemeral=True)
            return

        # the user_id might still not be a valid user id, it could be snowflake for something other than a user or simply a deleted user, so we test against that
        try:
            user = await self.client.fetch_user(user_id)
        except nextcord.NotFound:
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{user_id}` isn't a valid discord user id."), ephemeral=True)
            return

        # fail save in case for whatever reason the unban fails
        try:
            await interaction.guild.unban(user)
            await interaction.followup.send(embed=EmbedFunctions().success(f"{user.mention} has been unbanned."), ephemeral=True)
        except:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{user.mention} wasn't banned."), ephemeral=True)
            return

    ####################################################################################################

    @unban.on_autocomplete("user_id")
    async def autocomplete_unban(
        self,
        interaction: nextcord.Interaction,
        user_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""
        
        bans = await interaction.guild.bans(limit=None).flatten()

        all_bans_dict = {ban.user.id: ban.user.id for ban in bans}

        autocomplete_dict = Get.autocomplete_dict_from_search_string(user_id, all_bans_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot) -> None:
    client.add_cog(Ban(client))