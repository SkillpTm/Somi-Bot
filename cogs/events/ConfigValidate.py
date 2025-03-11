import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.utilities import SomiBot



class ConfigValidate(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def on_delete(self, input: nextcord.abc.GuildChannel | nextcord.Thread | nextcord.Role) -> None:
        """removes a channel/role from the Config, if it got deleted"""

        # check that the input was actually a channel/role
        if not isinstance(input, nextcord.TextChannel) and not isinstance(input, nextcord.Thread) and not isinstance(input, nextcord.Role):
            return

        if isinstance(input, nextcord.TextChannel) and isinstance(input, nextcord.Thread):
            if input.id == await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).server()).audit_log_get():
                await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).server()).audit_log_reset()

            if input.id in await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).hidden_channel()).get_list():
                await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).hidden_channel()).delete(input.id)

            if input.id in await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).level_ignore_channel()).get_list():
                await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).level_ignore_channel()).delete(input.id)
    
        elif isinstance(input, nextcord.Role):
            if input.id == await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).server()).default_role_get():
                await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).server()).default_role_reset()

            if [input.id == level_role[0] for level_role in await (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).level_role()).get_list()]:
                (await DBHandler(self.client.PostgresDB, server_id=input.guild.id).level_role()).delete(input.id)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigValidate(client))