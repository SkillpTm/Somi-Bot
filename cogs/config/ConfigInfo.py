import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get, LevelRoles
from lib.utilities import SomiBot



class ConfigInfo(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="info", description="get information on how this server is configured")
    async def config_info(self, interaction: nextcord.Interaction) -> None:
        """This command outputs a server's configuration info and some explanations."""

        self.client.Loggers.action_log(Get.log_message(interaction, "/config info"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        audit_log_output, default_role_output, hidden_channels_output, level_ignore_channels_output, level_roles_output = await self.get_config_data(interaction)

        AUDIT_LOG_INFO = "In the audit-log-channel you will get all logs the bot can provide, these include: delete log, edit log, join log, leave log, rename log and all mod activity.\n\n"
        DEFAULT_ROLE_INFO = "A default-role is a role every user should have. It will be given to any user (excluding bots) who joins this server.\n\n"
        HIDDEN_CHANNELS_INFO = "A hidden-channel deactivates keyword notifications, link-embeds and logs from this channel.\n\n"
        LEVEL_IGNORE_CHANNELS_INFO = "In a level-ignore-channel no one can earn any XP for levels.\n\n"
        LEVEL_ROLES_INFO = "A level-role is a role a user will get as soon as they reach a certain level. Their previous level-role will get removed from them.\n\n"

        embed = EmbedFunctions().builder(
            color = self.client.PERMISSION_COLOR,
            title = f"Configuration of: `{interaction.guild.name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Audit Log:",
                    AUDIT_LOG_INFO + audit_log_output,
                    False
                ],

                [
                    "Default Role:",
                    DEFAULT_ROLE_INFO + default_role_output,
                    False
                ],

                [
                    "Hidden Channels:",
                    HIDDEN_CHANNELS_INFO + hidden_channels_output,
                    False
                ],

                [
                    "Level Ignore Channels:",
                    LEVEL_IGNORE_CHANNELS_INFO + level_ignore_channels_output,
                    False
                ],

                [
                    "Level Roles:",
                    LEVEL_ROLES_INFO + level_roles_output,
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    ####################################################################################################

    async def get_config_data(self, interaction: nextcord.Interaction) -> tuple[str, str, str, str, str]:
        """This function gets all the data that can be configured and if there is none, it just replaces with a default text.
           It also validates that all channels/roles still exist and if not cleans up the db"""

        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()
        audit_log_output = ""

        if audit_log_id:
            if interaction.guild.get_channel(audit_log_id):
                audit_log_output = f"<#{audit_log_id}>"
            else:
                await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_reset()
        
        if not audit_log_output:
            audit_log_output = "`This server doesn't have a desginated channel for audit-Log messages.`"


        default_role_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_get()
        default_role_output = ""

        if default_role_id:
            if interaction.guild.get_role(default_role_id):
                default_role_output = f"<#{default_role_id}>"
            else:
                await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).default_role_reset()
        
        if not default_role_output:
            default_role_output = "`This server doesn't have a desginated default-role.`"


        hidden_channel_ids = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).hidden_channel()).get_list()
        hidden_channels_output = ""

        # check if all hidden channels still exits, the ones that do, get added to the output
        for index, hidden_channel_id in enumerate(hidden_channel_ids):
            if not interaction.guild.get_channel(hidden_channel_id):
                hidden_channel_ids.pop(index)
                await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).hidden_channel()).delete(hidden_channel_id)
                continue
            
            hidden_channels_output +=  f"<#{hidden_channel_id}>\n"

        if not hidden_channels_output:
            hidden_channels_output = "`This server doesn't have any hidden-channels.`"


        level_ignore_channel_ids = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).level_ignore_channel()).get_list()
        level_ignore_channels_output = ""

        # check if all level ignore channels still exits, the ones that do, get added to the output
        for index, level_ignore_channel_id in enumerate(level_ignore_channel_ids):
            if not interaction.guild.get_channel(level_ignore_channel_id):
                level_ignore_channel_ids.pop(index)
                await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).level_ignore_channel()).delete(level_ignore_channel_id)
                continue
            
            level_ignore_channels_output +=  f"<#{level_ignore_channel_id}>\n"

        if not level_ignore_channels_output:
            level_ignore_channels_output = "`This server doesn't have any level-ignore-channels.`"


        level_roles = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).level_role()).get_list()

        # check if all level roles still exits, the ones that do, get added to the output
        for index, level_role in enumerate(level_roles):
            if not interaction.guild.get_role(level_role[0]):
                level_roles.pop(index)
                await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).level_role()).delete(level_role[0])
                LevelRoles().update_users(self.client, interaction.guild)

        if level_roles:
            level_roles_output = LevelRoles.get_level_range_with_role(level_roles)

        else:
            level_roles_output = "`This server doesn't have any level-roles.`"


        return audit_log_output, default_role_output, hidden_channels_output, level_ignore_channels_output, level_roles_output



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigInfo(client))