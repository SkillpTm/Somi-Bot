import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class ConfigDefaultRole(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(Commands().data["config default-role"].name, Commands().data["config default-role"].description)
    async def config_default_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        action: typing.Literal["Set", "Reset"] = nextcord.SlashOption(
            Commands().data["config default-role"].parameters["action"].name,
            Commands().data["config default-role"].parameters["action"].description,
            required = True,
            choices = ["Set", "Reset"]
        ),
        role: nextcord.Role = nextcord.SlashOption(
            Commands().data["config default-role"].parameters["role"].name,
            Commands().data["config default-role"].parameters["role"].description,
            required = False
        )
    ) -> None:
        """This command sets/resets a default-role to the server. Meaning that on_member_join will apply this role automatically, if set"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if action == "Set":
            if not await self._set_role(interaction, role):
                return

            mod_action = f"{interaction.user.mention} set: {role.mention} as the new default-role."

        elif action == "Reset":
            if not (role := role or interaction.guild.get_role(await db.Server.DEFAULT_ROLE.get(interaction.guild.id) or 0)):
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("This server doesn't have a default-role to reset."))
                return

            if role != await db.Server.DEFAULT_ROLE.get(interaction.guild.id):
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("The role you provided is not this server's default-role."))
                return

            if not await self._reset_role(interaction, role):
                return

            mod_action = f"{interaction.user.mention} reset: {role.mention} as the default-role."

        if not (command_log := interaction.guild.get_channel(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0)): # type: ignore
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config default-role"].name}:",
                    mod_action,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    async def _set_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role
    ) -> bool:
        "sets or doesn't set the role indicated by the output bool"

        # check if an actual role was provided
        if not role:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("To set a new default-role you need to provide a role in the command."))
            return False

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner:  # type: ignore
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only make role the default-role, if the role is below your current top role!"))
            return False

        await db.Server.DEFAULT_ROLE.set(interaction.guild.id, role.id)
        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{role.mention} is from now on this server's default-role.\nThe role is being applied to users now, this can take a few minutes."))

        #apply the role to all users
        for member in interaction.guild.members:
            if role not in member.roles and not member.bot:
                await member.add_roles(role)

        return True


    async def _reset_role(
        self,
        interaction: nextcord.Interaction[SomiBot],
        role: nextcord.Role
    ) -> bool:
        "resets or doesn't reset the role indicated by the output bool"

        if interaction.user.top_role.position < role.position and interaction.user != interaction.guild.owner: # type: ignore
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only make role the default-role, if the role is below your current top role!"))
            return False

        await db.Server.DEFAULT_ROLE.set(interaction.guild.id, None)
        await interaction.followup.send(embed=EmbedFunctions().get_success_message("This server now doesn't have a default-role anymore.\nThe role is being removed from all users, this may take a few minutes."))

        # remove the role from all users
        for member in interaction.guild.members:
            if role in member.roles:
                await member.remove_roles(role)

        return True



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigDefaultRole(client))