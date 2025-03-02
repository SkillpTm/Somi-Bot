import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class ConfigDefaultRole(nextcord_C.Cog):

    def __init__(self, client) ->  None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "default-role", description = "set/unset a role someone gets upon joining this server")
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def config_default_role(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Set", "Unset"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            description = "the role to be set/unset",
            required = False
        )
    ) -> None:
        """This command sets/unsets a default-role to the server. Meaning that on_member_join will apply this role automatically, if set"""

        # just gets set so we don't error on stuff later
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

            #apply the role to all users
            for member in interaction.guild.members:
                if role not in member.roles and not member.bot:
                    await member.add_roles(role)

        elif action == "Unset":
            if role == interaction.guild.default_role:
                role = interaction.guild.get_role(await ConfigDB(interaction.guild.id, "DefaultRole").get_list(interaction.guild))

            if not await self._unsetRole(interaction, role):
                return
            
            mod_action = f"{interaction.user.mention} unset: <@&{role.id}> as the default-role."  

            # remove the role from all users
            for member in interaction.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
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

    @staticmethod
    async def _setRole(
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "sets or doesn't set the role indicated by the output bool"

        # check if an actual role was provided
        if role == interaction.guild.default_role:
            await interaction.followup.send(embed=EmbedFunctions().error("To set a new default-role you need to provide a role in the command."), ephemeral=True)
            return False

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only set a role as the default-role, if the role is below your current top role!"), ephemeral=True)
            return False
        
        added = ConfigDB(interaction.guild.id, "DefaultRole").add(role.id)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error("This server already has a default-role.\nUnset your default-role first."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} is from now on this server's default-role.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)
        return added

    ####################################################################################################

    @staticmethod
    async def _unsetRole(
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "unsets or doesn't unset the role indicated by the output bool"

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only unset a role as the default-role, if the role is below your current top role!"), ephemeral=True)
            return False

        deleted = ConfigDB(interaction.guild.id, "DefaultRole").delete(role.id)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error("This server doesn't have a default-role."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().success("This server now doesn't have a default-role anymore.\nThe role is being removed from all users, this may take a few minutes."), ephemeral=True)
        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigDefaultRole(client))