import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, LevelRoles
from lib.managers import Commands, Config
from lib.modules import SomiBot, YesNoButtons



class ConfigLevelRoles(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(
        Commands().data["config level-roles"].alias,
        Commands().data["config level-roles"].description,
        name_localizations = {country_tag: Commands().data["config level-roles"].name for country_tag in nextcord.Locale}
    )
    async def config_level_roles(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        action: typing.Literal["Add", "Remove", "Remove All"] = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["action"].name,
            Commands().data["config level-roles"].parameters["action"].description,
            required = True,
            choices = ["Add", "Remove", "Remove All"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["role"].name,
            Commands().data["config level-roles"].parameters["role"].description,
            required = False
        ),
        level: int = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["level"].name,
            Commands().data["config level-roles"].parameters["level"].description,
            required = False,
            min_value = 1,
            max_value = 1000
        )
    ) -> None:
        """This command adds/deletes a level-role to/from the server's level-roles"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if role and role.is_default():
            await interaction.send(embed=EmbedFunctions.get_error_message("You cannot set the @everyone role as the default-role."))
            return

        if role and interaction.user.top_role.position < role.position and interaction.user.id != interaction.guild.owner.id:  # type: ignore
            await interaction.send(embed=EmbedFunctions.get_error_message("You can only add/remove a role as a level-role, if the role is below your current top role!"))
            return

        if action == "Add":
            if not await self.add_role(interaction, role, level):
                return

            mod_action = f"{interaction.user.mention} added: {role.mention} as a level-role at level `{level}`."

        elif action == "Remove":
            if not await self.remove_role(interaction, role):
                return

            mod_action = f"{interaction.user.mention} removed: {role.mention} from the level-roles."

        elif action == "Remove All":
            if not await self.remove_all(interaction):
                return

            mod_action = f"{interaction.user.mention} removed **ALL** level-roles."


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions.builder(
            color = Config().PERMISSION_COLOR,
            author = "Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config level-roles"].full_name}:",
                    mod_action,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    async def add_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role,
        level: int
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not level:
            await interaction.send(embed=EmbedFunctions.get_error_message("You need to define a role **and** a level to add a new level-role."))
            return False

        if level in await db.LevelRole.LEVEL.get_all(where={db.LevelRole.SERVER: interaction.guild.id}):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"The level `{level}` already has a role assigned!\nTo get a list of all the level-roles use `/config info`."))
            return False

        if not (added := await db.LevelRole._.add({db.LevelRole.ID: role.id, db.LevelRole.LEVEL: level, db.LevelRole.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{role.mention} already has a level assigned or the level `{level}` already has a role assigned!\nTo get a list of all the level-roles use `/config info`."))
            return added

        await interaction.send(embed=EmbedFunctions.get_success_message(f"{role.mention} has been added to the level-roles.\nThe role is being applied to users now, this can take a few minutes."))

        await LevelRoles.update_users(interaction.guild) # type: ignore

        return added


    async def remove_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role
    ) -> bool:
        "removes or doesn't remove the role indicated by the output bool"

        if not role:
            await interaction.send(embed=EmbedFunctions.get_error_message("You need to define a role to remove a level-role."))
            return False

        if not (deleted := await db.LevelRole._.delete(role.id)):
            await interaction.send(embed=EmbedFunctions.get_error_message(f"{role.mention} isn't a level-role.\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return deleted

        await interaction.send(embed=EmbedFunctions.get_success_message(f"{role.mention} has been removed from the level-roles.\nThe level-roles are being re-applied to users now, this can take a few minutes."), ephemeral=True)

        await LevelRoles.update_users(interaction.guild) # type: ignore

        return deleted


    async def remove_all(self, interaction: nextcord.Interaction[SomiBot]) -> bool:
        """Removes all level-roles after user confirmation"""

        if not (level_roles := await db.LevelRole.ID.get_all(where={db.LevelRole.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions.get_error_message("There are no level-roles set.\nTo get a list of all the level-roles use `/config info`."))
            return False

        for role_id in level_roles:
            if interaction.user.top_role.position < interaction.guild.get_role(role_id).position and interaction.user.id != interaction.guild.owner.id: # type: ignore
                await interaction.send(embed=EmbedFunctions.get_error_message("You can only remove all level-roles, if all level-roles are below your current top role!"))
                return False

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions.get_info_message("Do you really want to remove **ALL** your level-roles __**(they can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions.get_error_message("Your level-roles have **not** been removed!"), ephemeral=True)
            return False

        await db.LevelRole._.delete(where={db.LevelRole.SERVER: interaction.guild.id}, limit=1_000_000)
        await interaction.send(embed=EmbedFunctions.get_success_message("**ALL** level-roles have been removed!"), ephemeral=True)

        return True



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelRoles(client))