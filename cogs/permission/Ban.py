import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.events.BanLog import BanLog
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot



class Ban(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["ban"].name,
        Commands().data["ban"].description,
        default_member_permissions = nextcord.Permissions(ban_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def ban(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["ban"].parameters["member"].name,
            Commands().data["ban"].parameters["member"].description,
            required = True
        ),
        delete_message_hours: int = nextcord.SlashOption(
            Commands().data["ban"].parameters["delete_message_hours"].name,
            Commands().data["ban"].parameters["delete_message_hours"].description,
            required = False,
            min_value = 0,
            max_value = 168,
            default = 1
        ),
        reason: str = nextcord.SlashOption(
            Commands().data["ban"].parameters["reason"].name,
            Commands().data["ban"].parameters["reason"].description,
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command bans a member, while providing a delete message amount (in seconds) and giving a reason. It also protects from self-bans."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.send(embed=EmbedFunctions.get_error_message("You can't ban yourself!"))
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.guild.owner: # type: ignore
            await interaction.send(embed=EmbedFunctions.get_error_message("You can only ban a member, if your current top-role is above their current top-role!"))
            return

        await interaction.guild.ban(user=member, reason=reason, delete_message_seconds=delete_message_hours * 60 * 60)
        await interaction.send(embed=EmbedFunctions.get_success_message(f"Succesfully banned {member.mention}."))
        await BanLog.send_ban_log(interaction.guild, interaction.user, member, reason) # type: ignore


    @nextcord.slash_command(
        Commands().data["unban"].name,
        Commands().data["unban"].description,
        default_member_permissions = nextcord.Permissions(ban_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def unban(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user_id: str = nextcord.SlashOption(
            Commands().data["unban"].parameters["user_id"].name,
            Commands().data["unban"].parameters["user_id"].description,
            required = True,
            min_length = 18,
            max_length = 19
        ),
        reason: str = nextcord.SlashOption(
            Commands().data["unban"].parameters["reason"].name,
            Commands().data["unban"].parameters["reason"].description,
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command unbans a user, if that user exists and was banned."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not user_id.isdigit():
            await interaction.send(embed=EmbedFunctions.get_error_message(f"`{user_id}` isn't a valid discord user id."))
            return

        # the user_id might still not be a valid user id, it could be snowflake for something other than a user or simply a deleted user, so we test against that
        try:
            user = await self.client.fetch_user(int(user_id))
        except nextcord.NotFound:
            await interaction.send(embed=EmbedFunctions.get_error_message(f"`{user_id}` isn't a valid discord user id."))
            return

        # fail save in case for whatever reason the unban fails
        try:
            await interaction.guild.unban(user, reason=reason)
            await interaction.send(embed=EmbedFunctions.get_success_message(f"{user.mention} has been unbanned."))
        except nextcord.Forbidden:
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{user.mention} wasn't unbanned."))
            return

        await BanLog.send_unban_log(interaction.guild, interaction.user, user, reason) # type: ignore


    @unban.on_autocomplete("user_id")
    async def unban_autocomplete_user_id(
        self,
        interaction: nextcord.Interaction[SomiBot],
        user_id: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                user_id,
                {f"{ban.user.id}: {ban.user.name}": str(ban.user.id) async for ban in interaction.guild.bans()}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Ban(client))