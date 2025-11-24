import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, LevelRoles
from lib.managers import Commands, Config
from lib.modules import SomiBot



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
        action: typing.Literal["Add", "Remove"] = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["action"].name,
            Commands().data["config level-roles"].parameters["action"].description,
            required = True,
            choices = ["Add", "Remove"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["role"].name,
            Commands().data["config level-roles"].parameters["role"].description,
            required = True
        ),
        level: int = nextcord.SlashOption(
            Commands().data["config level-roles"].parameters["level"].name,
            Commands().data["config level-roles"].parameters["level"].description,
            required = False,
            min_value = 2,
            max_value = 1000
        )
    ) -> None:
        """This command adds/deletes a level-role to/from the server's level-roles"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:  # type: ignore
            await interaction.send(embed=EmbedFunctions().get_error_message("You can only add/remove a role as a level-role, if the role is below your current top role!"))
            return

        if action == "Add":
            if not await self._add_role(interaction, role, level):
                return

            mod_action = f"{interaction.user.mention} added: {role.mention} as a level-role at level `{level}`."

        elif action == "Remove":
            if not await self._remove_role(interaction, role):
                return

            mod_action = f"{interaction.user.mention} removed: {role.mention} from the level-roles."


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config level-roles"].name}:",
                    mod_action,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    async def _add_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role,
        level: int
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not level:
            await interaction.send(embed=EmbedFunctions().get_error_message("You need to define a role **and** a level to add a new level-role."))
            return False

        if not (added := await db.LevelRole._.add({db.LevelRole.ID: role.id, db.LevelRole.LEVEL: level, db.LevelRole.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{role.mention} already has a level assigned or the level `{level}` already has a role assigned!\nTo get a list of all the level-roles use `/config info`."))
            return added

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{role.mention} has been added to the level-roles.\nThe role is being applied to users now, this can take a few minutes."))

        await LevelRoles.update_users(interaction.guild) # type: ignore

        return added


    async def _remove_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role
    ) -> bool:
        "removes or doesn't remove the role indicated by the output bool"

        if not (deleted := await db.LevelRole._.delete(interaction.guild.id, role.id)):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{role.mention} isn't a level-role.\nTo get a list of all the level-roles use `/config info`."), ephemeral=True)
            return deleted

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{role.mention} has been removed from the level-roles.\nThe level-roles are being re-applied to users now, this can take a few minutes."), ephemeral=True)

        await LevelRoles.update_users(interaction.guild) # type: ignore

        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelRoles(client))