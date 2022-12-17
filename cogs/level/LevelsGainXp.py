####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import re
import time

####################################################################################################

from lib.db_modules import LevelsDB, LevelIgnoreChannelsDB
from lib.modules import Checks, LevelRoles
from lib.utilities import SomiBot



class LevelsGainXp(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord_C.Cog.listener()
    async def on_message(self,
                         message: nextcord.Message):
        """This command gives xp to a user on the server the message was send, if the message:
            1. is longer than 10 characters
            2. was not send in a levels ignore channel
            3. was send after the user's cooldown went off
            
            afterwards the command will try to apply levelroles"""                 

        if not Checks.message_in_guild(self.client, message):
            return

        if not len(re.sub('<[^ ]+?>', "",message.content)) > 10:
            return

        ignore_channel_ids = LevelIgnoreChannelsDB().channels_list(message.guild)

        if message.channel.id in ignore_channel_ids:
            return

        LevelsDB().insert_user(message.guild.id, message.author.id)

        cooldown_time = LevelsDB().get_user_cooldown(message.guild.id, message.author.id)

        if cooldown_time >= int(time.time()):
            return

        LevelsDB().increase_user_xp(message.guild.id, message.author.id)

        user_level, xp_until_next_level =  LevelsDB().get_user_level(message.guild.id, message.author.id)

        await LevelRoles().apply(message.guild, [[message.author.id, user_level]])



def setup(client: SomiBot):
    client.add_cog(LevelsGainXp(client))