####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import AuditLogChannelDB, DefaultRoleDB, HiddenChannelsDB, LevelIgnoreChannelsDB, LevelRolesDB
from lib.modules import Checks, EmbedFunctions, LevelRoles
from lib.utilities import SomiBot



class ConfigInfo(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "info", description = "get information on how this server is configured")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def config_info(self,
                          interaction: nextcord.Interaction):
        """This command outputs a server's configuration info and some explanations."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /config info")

        await interaction.response.defer(ephemeral=True, with_message=True)

        audit_log_output, default_role_output, hidden_channels_output, level_ignore_channels_output, level_roles_output = await self.get_config_data(interaction)

        AUDIT_LOG_INFO = "In the audit-log-channel you will get all logs the bot can provide, these include: delete log, edit log, join log, leave log, rename log and all mod activity.\n\n"
        DEFAULT_ROLE_INFO = "A default-role is a role every user should have. It will be given to any user (excluding bots) who joins this server.\n\n"
        HIDDEN_CHANNELS_INFO = "A hidden-channel deactivates keyword notifications, link-embeds and logs from this channel.\n\n"
        LEVEL_IGNORE_CHANNELS_INFO = "In a level-ignore-channel no one can earn any XP for levels.\n\n"
        LEVEL_ROLES_INFO = "A level-role is a role a user will get as soon as they reach a certain level. Their previous level-role will get removed from them.\n\n"

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
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

    @staticmethod
    async def get_config_data(interaction: nextcord.Interaction) -> tuple[str, str, str, str, str]:
        """This function gets all the data that can be configured and if there is none, it just replaces with a default text."""

        audit_log_id = AuditLogChannelDB().get(interaction.guild)

        if audit_log_id:
            audit_log_output = f"<#{audit_log_id}>"
        else:
            audit_log_output = "`This server doesn't have a desginated channel for audit Log messages.`"


        default_role_id = DefaultRoleDB().get(interaction.guild)

        if default_role_id:
            default_role_output = f"<@&{default_role_id}>"
        else:
            default_role_output = "`This server doesn't have a desginated default role.`"


        hidden_channel_ids = HiddenChannelsDB().channels_list(interaction.guild)

        if hidden_channel_ids != []:
            hidden_channels_output = ""

            for hidden_channel_id in hidden_channel_ids:
                hidden_channels_output +=  f"<#{hidden_channel_id}>\n"

        else:
            hidden_channels_output = "`This server doesn't have any hidden-channels.`"


        level_ignore_channel_ids = LevelIgnoreChannelsDB().channels_list(interaction.guild)

        if level_ignore_channel_ids != []:
            level_ignore_channels_output = ""

            for level_ignore_channel_id in level_ignore_channel_ids:
                level_ignore_channels_output +=  f"<#{level_ignore_channel_id}>\n"

        else:
            level_ignore_channels_output = "`This server doesn't have any level-ignore-channels.`"


        level_roles = await LevelRolesDB().roles_list(interaction.guild)

        if level_roles != []:
            level_roles_output = LevelRoles().get_level_range_with_role(level_roles)

        else:
            level_roles_output = "`This server doesn't have any level-roles.`"


        return audit_log_output, default_role_output, hidden_channels_output, level_ignore_channels_output, level_roles_output



def setup(client: SomiBot):
    client.add_cog(ConfigInfo(client))