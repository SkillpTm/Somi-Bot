import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, SomiBot



class Close(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "close",
        description = "removes send message perms from @everyone and the default role, on the roles, also pauses invites",
        default_member_permissions = nextcord.Permissions(manage_roles=True, manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def close(self, interaction: nextcord.Interaction) -> None:
        """This command takes the send-messages permission from the default-role away, effectifly closing down the server. Additionally it sets invites_disabled = True"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/close"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        default_role_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_get()

        roles_to_modify = [interaction.guild.default_role]

        if default_role_id:
            roles_to_modify.append(interaction.guild.get_role(default_role_id))

        permissions_to_check: list[bool] = []

        for role in roles_to_modify:
            permissions_to_check = (role.permissions.send_messages, role.permissions.send_messages_in_threads, role.permissions.add_reactions)

        # if all relevant permissions are already turned off, the server is already closed
        if all(not permission for permission in permissions_to_check):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("The server is already closed.\n To re-open it use `/open`"), ephemeral=True)
            return

        await interaction.guild.edit(invites_disabled = True)

        for role in roles_to_modify:
            await role.edit(
                permissions = nextcord.Permissions(
                    permissions = role.permissions.value,
                    send_messages = False,
                    send_messages_in_threads = False,
                    add_reactions = False
                )
            )

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("Closed the server sucessfully.\n To re-open it use `/open`"), ephemeral=True)


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.dark_red(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
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
        name = "open",
        description = "gives back send message perms for @everyone and the default role, on the roles, also pauses invites",
        default_member_permissions = nextcord.Permissions(manage_roles=True, manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def open(self, interaction: nextcord.Interaction) -> None:
        """This command gives the send-messages permission back to the default-role, effectifly opening the server back up."""

        self.client.Loggers.action_log(Get.log_message(interaction, "/open"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        default_role_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_get()

        roles_to_modify = [interaction.guild.default_role]

        if default_role_id:
            roles_to_modify.append(interaction.guild.get_role(default_role_id))

        permissions_to_check: list[bool] = []

        for role in roles_to_modify:
            permissions_to_check = (role.permissions.send_messages, role.permissions.send_messages_in_threads, role.permissions.add_reactions)

        # if all relevant permissions are already turned on, the server is already open
        if all(permission for permission in permissions_to_check):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("The server is already open.\n To close it use `/close`"), ephemeral=True)
            return

        await interaction.guild.edit(invites_disabled = False)

        for role in roles_to_modify:
            await role.edit(
                permissions = nextcord.Permissions(
                    permissions = role.permissions.value,
                    send_messages = True,
                    send_messages_in_threads = True,
                    add_reactions = True
                )
            )

            for channel in interaction.guild.channels:
                if not channel.type in Lists.TEXT_CHANNELS:
                    continue

                if not channel.permissions_for(interaction.guild.get_member(self.client.user.id)).manage_channels:
                    continue

                overwrites = channel.overwrites_for(role)
                overwrites.send_messages = True
                overwrites.send_messages_in_threads = True
                overwrites.add_reactions = True

                await channel.set_permissions(target=role, overwrite=overwrites)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("Re-opened the server sucessfully."), ephemeral=True)


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.dark_red(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
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