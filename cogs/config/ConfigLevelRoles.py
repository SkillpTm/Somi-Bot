import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get, LevelRoles
from lib.utilities import SomiBot



class ConfigLevelRoles(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "level-roles", description = "set a role to be given, when a certain level is reached")
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def config_level_roles(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Add", "Remove"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            description = "the role users should/ the role to be deleted",
            required = True
        ),
        level: int = nextcord.SlashOption(
            description = "the level you're supposed to get a role",
            required = False,
            min_value = 2,
            max_value = 1000
        )
    ) -> None:
        """This command adds/deletes a level-role to/from the server's level-roles"""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/config level-ignore-channel",
            {"action": action, "role": str(role.id), "level": str(level)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.top_role.position < role.position and interaction.user != interaction.user.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only add/remove a role as a level-role, if the role is below your current top role!"), ephemeral=True)
            return


        if action == "Add":
            if not await self.addRole(interaction, role, level):
                return
            
            mod_action = f"{interaction.user.mention} added: {role.mention} as a level-role at level `{level}`."
            await LevelRoles().apply(interaction.guild)
            

        elif action == "Remove":
            if not await self.removeRole(interaction, role):
                return
            
            mod_action = f"{interaction.user.mention} removed: {role.mention} from the level-roles."  
            await LevelRoles().remove_from_members(interaction.guild, role)


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
                    "/config level-roles:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)


    ####################################################################################################

    @staticmethod
    async def addRole(
        interaction: nextcord.Interaction,
        role: nextcord.Role,
        level: int
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not level:
            await interaction.followup.send(embed=EmbedFunctions().error("You need to define a role **and** a level to add a new level-role."), ephemeral=True)
            return False

        added = ConfigDB(interaction.guild.id, "LevelRoles").add(role.id, level)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{role.mention} already has a level assigned or the level `{level}` already has a role assigned!\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} has been added to the level-roles.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)
        return added

    ####################################################################################################

    @staticmethod
    async def removeRole(
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "removes or doesn't remove the role indicated by the output bool"

        deleted = ConfigDB(interaction.guild.id, "LevelRoles").delete(role.id)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{role.mention} isn't a level-role.\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().success(f"{role.mention} has been removed from the level-roles.\nThe level-roles are being re-applied to users now, this can take a few minutes."), ephemeral=True)
        return deleted


def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelRoles(client))