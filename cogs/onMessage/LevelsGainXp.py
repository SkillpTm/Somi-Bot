import nextcord
import nextcord.ext.commands as nextcord_C
import re

from lib.dbModules import DBHandler
from lib.modules import Checks, LevelRoles
from lib.utilities import SomiBot



class LevelsGainXp(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def levels_gain_xp(self, message: nextcord.Message) -> None:
        """This command gives xp to a user on the server the message was send, if the message:
            1. is longer than 10 characters
            2. was not send in a levels ignore channel
            3. was send after the user's cooldown went off
            
            afterwards the command will try to apply levelroles"""                 

        if not Checks.message_in_guild(self.client, message):
            return

        # re removes emotes, make sure messages are above 10 chars
        if not len(re.sub('<[^ ]+?>', "",message.content)) > 10:
            return

        # make sure message isn't in a levels ignore channel
        if message.channel.id in await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).level_ignore_channel()).get_list():
            return

        if not await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).level()).increase_xp():
            return

        user_level, _ =  await (await DBHandler(self.client.PostgresDB, server_id=message.guild.id).level()).get_level_and_xp_until_next()

        await LevelRoles().apply(message.guild, [[message.author.id, user_level]])



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsGainXp(client))