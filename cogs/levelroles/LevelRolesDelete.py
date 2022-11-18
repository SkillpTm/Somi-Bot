###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_levelroles import check_levelroles_for_server_role_and_level, delete_level_role
from utilities.maincommands import checks
from utilities.partial_commands import remove_level_roles_from_members
from utilities.variables import MODERATOR_ID



class LevelRolesDelete(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import level_roles

    ###level#roles#delete###########################################################

    @level_roles.subcommand(name = "delete", description = "[MOD] stop people getting a role after reaching a certain level")
    @nextcord.ext.application_checks.has_permissions(manage_roles=True)
    async def level_roles_delete(self,
                                 interaction: nextcord.Interaction,
                                 *,
                                 role: nextcord.Role = nextcord.SlashOption(description="the role users should get at the set level", required=True)):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /level-roles delete {role.name}")

        if not interaction.user.guild.owner and interaction.user.top_role.position <= role.position:
            await interaction.response.send_message("You can only delete roles from levelroles, if they are below your current top role!", ephemeral=True)
            return

        already_used = check_levelroles_for_server_role_and_level(interaction.guild.id, role.id)

        if not already_used:
            await interaction.response.send_message(f"The role {role.mention} doesn't have a level assigned!", ephemeral=True)
            return

        delete_level_role(interaction.guild.id, role.id)

        await remove_level_roles_from_members(interaction.guild, role)

        await interaction.response.send_message(f"The role {role.mention} won't be given out anymore and the levelroles have been re-applied.", ephemeral=True)     

        uses_update("mod_command_uses", "level-roles delete")

    @level_roles_delete.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(LevelRolesDelete(client))