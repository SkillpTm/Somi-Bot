import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class ConfigDefaultRole(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) ->  None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="default-role", description="set/reset a role someone gets upon joining this server")
    async def config_default_role(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Set", "Reset"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            description = "the role to be set/reset",
            required = False
        )
    ) -> None:
        """This command sets/resets a default-role to the server. Meaning that on_member_join will apply this role automatically, if set"""

        # just gets set to the default_role so we don't error on stuff later
        if not role:
            role = interaction.guild.default_role

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/config default-role",
            {"action": action, "role": str(role.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Set":
            if not await self._setRole(interaction, role):
                return
            
            mod_action = f"{interaction.user.mention} set: {role.mention} as the new default-role."

        elif action == "Reset":
            if role.id == interaction.guild.default_role.id:
                role = interaction.guild.get_role(await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_get())

            if not await self._resetRole(interaction, role):
                return
            
            mod_action = f"{interaction.user.mention} reset: {role.mention} as the default-role."  


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config default-role:",
                    mod_action,
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

    ####################################################################################################

    async def _setRole(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "sets or doesn't set the role indicated by the output bool"

        # check if an actual role was provided
        if role.id == interaction.guild.default_role.id:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("To set a new default-role you need to provide a role in the command."), ephemeral=True)
            return False
        
        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only make role the default-role, if the role is below your current top role!"), ephemeral=True)
            return False
        
        await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_set(role.id)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{role.mention} is from now on this server's default-role.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)

        #apply the role to all users
        for member in interaction.guild.members:
            if role not in member.roles and not member.bot:
                await member.add_roles(role)

        return True

    ####################################################################################################

    async def _resetRole(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "resets or doesn't reset the role indicated by the output bool"

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only make role the default-role, if the role is below your current top role!"), ephemeral=True)
            return False

        deleted = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_reset()

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("This server doesn't have a default-role."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("This server now doesn't have a default-role anymore.\nThe role is being removed from all users, this may take a few minutes."), ephemeral=True)

        # remove the role from all users
        for member in interaction.guild.members:
            if role in member.roles:
                await member.remove_roles(role)

        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigDefaultRole(client))