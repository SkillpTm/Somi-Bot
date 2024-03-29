####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class ConfigDefaultRole(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "default-role", description = "set/unset a role someone gets upon joining this server")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def config_default_role(self,
                                  interaction: nextcord.Interaction,
                                  *,
                                  action: str = nextcord.SlashOption(description="which action do you want to take", required=True, choices=["Set", "Unset"]),
                                  role: nextcord.Role = nextcord.SlashOption(description="the role to be set/unset", required=False)):
        """This command sets/unsets a default-role to the server. Meaning that on_member_join will apply this role automatically, if set"""

        if not role:
            role = interaction.guild.default_role

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /config default-role {action}: {role.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Set":
            if role == interaction.guild.default_role:
                await interaction.followup.send(embed=EmbedFunctions().error("To set a new default-role you need to provide a role in the command."), ephemeral=True)
                return

            if interaction.user.top_role.position < role.position and interaction.user != interaction.user.guild.owner:
                await interaction.followup.send(embed=EmbedFunctions().error("You can only set a role as the default-role, if the role is below your current top role!"), ephemeral=True)
                return
            
            added = ConfigDB(interaction.guild.id, "DefaultRole").add(role.id)

            if not added:
                await interaction.followup.send(embed=EmbedFunctions().error("This server already has a default-role.\nUnset your default-role first."), ephemeral=True)
                return

            await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} is from now on this server's default-role.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)

            mod_action = f"{interaction.user.mention} set: {role.mention} as the new default-role."

            for member in interaction.guild.members:
                if role not in member.roles and not member.bot:
                    await member.add_roles(role)


        elif action == "Unset":
            role_id: int = await ConfigDB(interaction.guild.id, "DefaultRole").get_list(interaction.guild)
            deleted = ConfigDB(interaction.guild.id, "DefaultRole").delete(role_id)

            if not deleted:
                await interaction.followup.send(embed=EmbedFunctions().error("This server doesn't have a default-role."), ephemeral=True)
                return

            role = interaction.guild.get_role(role_id)

            if interaction.user.top_role.position < role.position and interaction.user != interaction.user.guild.owner:
                await interaction.followup.send(embed=EmbedFunctions().error("You can only unset a role as the default-role, if the role is below your current top role!"), ephemeral=True)
                return

            await interaction.followup.send(embed=EmbedFunctions().success("This server now doesn't have a default-role anymore.\nThe role is being removed from all users, this may take a few minutes."), ephemeral=True)  

            mod_action = f"{interaction.user.mention} unset: <@&{role.id}> as the default-role."  

            for member in interaction.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config default-role:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(ConfigDefaultRole(client))