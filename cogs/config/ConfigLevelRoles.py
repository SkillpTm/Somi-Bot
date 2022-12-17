###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_levelroles import check_levelroles_for_server_role_and_level, add_role_to_level
from utilities.maincommands import checks
from utilities.partial_commands import level_roles_apply
from utilities.variables import MODERATOR_ID



class LevelRolesAdd(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import level_roles

    ###level#roles#add###########################################################

    @level_roles.subcommand(name = "add", description = "[MOD] set a role to be given, when a certain level is reached")
    @nextcord.ext.application_checks.has_permissions(manage_roles=True)
    async def level_roles_add(self,
                              interaction: nextcord.Interaction,
                              *,
                              role: nextcord.Role = nextcord.SlashOption(description="the role users should get at the set level", required=True),
                              level: int = nextcord.SlashOption(description="the level you're supposed to get a role", required=True, min_value=2, max_value=1000)):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /level-roles add {role.name} {level}")

        if interaction.user.top_role.position < role.position and interaction.user != interaction.user.guild.owner:
            await interaction.response.send_message("You can only add roles to levelroles, if they are below your current top role!", ephemeral=True)
            return

        already_used = check_levelroles_for_server_role_and_level(interaction.guild.id, role.id, level)

        if already_used:
            await interaction.response.send_message(f"The role {role.mention} already has a level assigned or the level `{level}` already has a role assugned!", ephemeral=True)
            return

        add_role_to_level(interaction.guild.id, role.id, level)

        await level_roles_apply(interaction.guild)

        await interaction.response.send_message(f"The role {role.mention} has been added and applied as a new levelrole in this server!", ephemeral=True)     

        uses_update("mod_command_uses", "level-roles add")

    @level_roles_add.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(LevelRolesAdd(client))