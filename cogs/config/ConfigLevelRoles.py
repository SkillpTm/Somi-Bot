####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import AuditLogChannelDB, LevelRolesDB
from lib.modules import Checks, EmbedFunctions, LevelRoles
from lib.utilities import SomiBot



class ConfigLevelRoles(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "level-roles", description = "set a role to be given, when a certain level is reached")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def config_level_roles(self,
                                 interaction: nextcord.Interaction,
                                 *,
                                 action: str = nextcord.SlashOption(description="which action do you want to take", required=True, choices=["Add", "Remove"]),
                                 role: nextcord.Role = nextcord.SlashOption(description="the role users should/ the role to be deleted", required=True),
                                 level: int = nextcord.SlashOption(description="the level you're supposed to get a role", required=False, min_value=2, max_value=1000)):
        """This command adds/deletes a level-role to/from the server's level-roles"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /config level-roles {action} {role.id} {level}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.top_role.position < role.position and interaction.user != interaction.user.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only add/remove a role as a level-role, if the role is below your current top role!"), ephemeral=True)
            return


        if action == "Add":
            if not level:
                await interaction.followup.send(embed=EmbedFunctions().error("You need to define a role **and** a level to add a new level-role."), ephemeral=True)
                return

            already_used = LevelRolesDB().check_role_or_level_inserted(interaction.guild.id, role.id, level)

            if already_used:
                await interaction.followup.send(embed=EmbedFunctions().error(f"{role.mention} already has a level assigned or the level `{level}` already has a role assigned!\nTo get a list of all level-roles use `/config info`."), ephemeral=True)
                return

            LevelRolesDB().insert_role(interaction.guild.id, role.id, level)

            await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} has been added to the level-roles.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)
            
            await LevelRoles().apply(interaction.guild)
            

        elif action == "Remove":
            already_used = LevelRolesDB().check_role_or_level_inserted(interaction.guild.id, role.id)

            if not already_used:
                await interaction.followup.send(embed=EmbedFunctions().error(f"{role.mention} isn't a level-role.\nTo get a list of all level-roles use `/config info`."), ephemeral=True)
                return

            LevelRolesDB().delete_role(interaction.guild.id, role.id)

            await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} has been removed from the level-roles.\nThe level-roles are being applied to users now, this can take a few minutes."), ephemeral=True)

            await LevelRoles().remove_from_members(interaction.guild, role)


        audit_log_id = AuditLogChannelDB().get(interaction.guild)

        if not audit_log_id:
            return

        if action == "Add":
            mod_action = f"{interaction.user.mention} added: {role.mention} as a level-role at level `{level}`."   
        elif action == "Remove":
            mod_action = f"{interaction.user.mention} removed: {role.mention} from the level-roles."  

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config level-roles:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)


def setup(client: SomiBot):
    client.add_cog(ConfigLevelRoles(client))