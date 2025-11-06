import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get, LevelRoles
from lib.utilities import SomiBot



class ConfigLevelRoles(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="level-roles", description="set a role to be given, when a certain level is reached")
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
            description = "the level you're supposed to get a role at",
            required = False,
            min_value = 2,
            max_value = 1000
        )
    ) -> None:
        """This command adds/deletes a level-role to/from the server's level-roles"""

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/config level-ignore-channel",
            {"action": action, "role": str(role.id), "level": str(level)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only add/remove a role as a level-role, if the role is below your current top role!"), ephemeral=True)
            return

        if action == "Add":
            if not await self._add_role(interaction, role, level):
                return

            mod_action = f"{interaction.user.mention} added: {role.mention} as a level-role at level `{level}`."

        elif action == "Remove":
            if not await self._remove_role(interaction, role):
                return

            mod_action = f"{interaction.user.mention} removed: {role.mention} from the level-roles."


        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = self.client.config.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/config level-roles:",
                    mod_action,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)


    ####################################################################################################

    async def _add_role(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role,
        level: int
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not level:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You need to define a role **and** a level to add a new level-role."), ephemeral=True)
            return False

        if not (added := await (await DBHandler(self.client.database, server_id=interaction.guild.id).level_role()).add(role.id, level)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{role.mention} already has a level assigned or the level `{level}` already has a role assigned!\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{role.mention} has been added to the level-roles.\nThe role is being applied to users now, this can take a few minutes."), ephemeral=True)

        await LevelRoles().update_users(self.client, interaction.guild)

        return added

    ####################################################################################################

    async def _remove_role(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role
    ) -> bool:
        "removes or doesn't remove the role indicated by the output bool"

        if not (deleted := await (await DBHandler(self.client.database, server_id=interaction.guild.id).level_role()).delete(role.id)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{role.mention} isn't a level-role.\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{role.mention} has been removed from the level-roles.\nThe level-roles are being re-applied to users now, this can take a few minutes."), ephemeral=True)

        await LevelRoles().update_users(self.client, interaction.guild)

        return deleted


def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelRoles(client))