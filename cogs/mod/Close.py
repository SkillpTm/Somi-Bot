import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Close(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "close",
        description = "takes all users through the default-role the send-messages permission away",
        default_member_permissions = nextcord.Permissions(manage_roles=True, manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def close(self, interaction: nextcord.Interaction) -> None:
        """This command takes the send-messages permission from the default-role away, effectifly closing down the server. Additionally it sets invites_disabled = True"""

        self.client.Loggers.action_log(Get().log_message(interaction, "/close"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        default_role_id: int = await ConfigDB(interaction.guild.id, "DefaultRole").get_list(interaction.guild)

        # if there hasn't been a default role set in Somi, use @everyone
        if not default_role_id:
            default_role_id = interaction.guild.default_role.id

        default_role = interaction.guild.get_role(default_role_id)

        permissions_to_check = (default_role.permissions.send_messages, default_role.permissions.send_messages_in_threads, default_role.permissions.add_reactions)

        # if all relevant permissions are already turned off, the server is already closed
        if all(not permission for permission in permissions_to_check):
            await interaction.followup.send(embed=EmbedFunctions().error("The server is already closed.\n To re-open it use `/open`"), ephemeral=True)
            return

        await interaction.guild.edit(invites_disabled = True)
        await default_role.edit(permissions=nextcord.Permissions(permissions = default_role.permissions.value, send_messages = False, send_messages_in_threads = False, add_reactions = False))

        await interaction.followup.send(embed=EmbedFunctions().success("Closed the server sucessfully.\n To re-open it use `/open`"), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.dark_red(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/close:",
                    f"{interaction.user.mention} closed the server!",
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

    ####################################################################################################

    @nextcord.slash_command(
        name = "unclose",
        description = "gives users through the default-role the send-messages permission back",
        default_member_permissions = nextcord.Permissions(manage_roles=True, manage_guild=True),
        name_localizations = {country_tag:"open" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def open(self, interaction: nextcord.Interaction) -> None:
        """This command gives the send-messages permission back to the default-role, effectifly opening the server back up."""

        self.client.Loggers.action_log(Get().log_message(interaction, "/open"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        default_role_id: int = await ConfigDB(interaction.guild.id, "DefaultRole").get_list(interaction.guild)

        # if there hasn't been a default role set in Somi, use @everyone
        if not default_role_id:
            default_role_id = interaction.guild.default_role.id

        default_role = interaction.guild.get_role(default_role_id)

        permissions_to_check = (default_role.permissions.send_messages, default_role.permissions.send_messages_in_threads, default_role.permissions.add_reactions)

        # if all relevant permissions are already turned on, the server is already open
        if all(permission for permission in permissions_to_check):
            await interaction.followup.send(embed=EmbedFunctions().error("The server is already open.\n To close it use `/close`"), ephemeral=True)
            return

        await interaction.guild.edit(invites_disabled = False)
        await default_role.edit(permissions=nextcord.Permissions(permissions = default_role.permissions.value, send_messages = True, send_messages_in_threads = True, add_reactions = True))

        await interaction.followup.send(embed=EmbedFunctions().success("Re-opened the server sucessfully."), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.dark_red(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/open:",
                    f"{interaction.user.mention} re-opened the server!",
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Close(client))