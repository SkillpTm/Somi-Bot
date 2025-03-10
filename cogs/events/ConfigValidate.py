import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.utilities import SomiBot



class ConfigValidate(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def remove_channel(self, channel: nextcord.abc.GuildChannel | nextcord.Thread) -> None:
        """removes a channel from AuditLogChannel, Hiddenchannels and LevelgnoreChannels"""

        if not isinstance(channel, nextcord.TextChannel) and not isinstance(channel, nextcord.Thread):
            return

        if channel.id == await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).server()).audit_log_get():
            await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).server()).audit_log_reset()

        if channel.id in await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).hidden_channel()).get_list():
            await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).hidden_channel()).delete(channel.id)

        if channel.id in await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).level_ignore_channel()).get_list():
            await (await DBHandler(self.client.PostgresDB, server_id=channel.guild.id).level_ignore_channel()).delete(channel.id)

    ####################################################################################################

    async def remove_role(self, role: nextcord.Role) -> None:
        """removes a role from DefaultRole and LevelRoles"""

        if role.id == await (await DBHandler(self.client.PostgresDB, server_id=role.guild.id).server()).default_role_get():
            await (await DBHandler(self.client.PostgresDB, server_id=role.guild.id).server()).default_role_reset()

        if [role.id == level_role[0] for level_role in await (await DBHandler(self.client.PostgresDB, server_id=role.guild.id).level_role()).get_list()]:
            (await DBHandler(self.client.PostgresDB, server_id=role.guild.id).level_role()).delete(role.id)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigValidate(client))