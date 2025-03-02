import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import ConfigDB
from lib.utilities import SomiBot



class ConfigValidate(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def remove_channel(self, channel: nextcord.abc.GuildChannel | nextcord.Thread) -> None:
        """removes a channel from AuditLogChannel, Hiddenchannels and LevelgnoreChannels"""

        if not isinstance(channel, nextcord.TextChannel) and not isinstance(channel, nextcord.Thread):
            return

        if await channel.id == ConfigDB(channel.guild.id, "AuditLogChannel").get_list(channel.guild):
            ConfigDB(channel.guild.id, "AuditLogChannel").delete(channel.id)

        if await channel.id in ConfigDB(channel.guild.id, "HiddenChannels").get_list(channel.guild):
            ConfigDB(channel.guild.id, "HiddenChannels").delete(channel.id)

        if await channel.id in ConfigDB(channel.guild.id, "LevelIgnoreChannels").get_list(channel.guild):
            ConfigDB(channel.guild.id, "LevelIgnoreChannels").delete(channel.id)

    ####################################################################################################

    async def remove_role(self, role: nextcord.Role) -> None:
        """removes a role from DefaultRole and LevelRoles"""

        if await role.id == ConfigDB(role.guild.id, "DefaultRole").get_list(role.guild):
            ConfigDB(role.guild.id, "DefaultRole").delete(role.id)

        if [role.id == level_role[0] for level_role in await ConfigDB(role.guild.id, "LevelRoles").get_list(role.guild)]:
            ConfigDB(role.guild.id, "LevelRoles").delete(role.id)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigValidate(client))