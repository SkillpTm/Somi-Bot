###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_levels import check_level_for_server_and_user, get_user_cooldown, increase_user_xp, get_user_level
from database.database_levels_ignore import make_ignore_channel_table, ignore_channels_list
from database.database_levelroles import check_levelroles_for_server_role_and_level
from utilities.maincommands import checks
from utilities.partial_commands import level_roles_apply



class LevelsGainXp(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###gain#xp###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_message(self,
                         message: nextcord.Message):
        if not checks(self.client, message.guild, message.author):
            return

        if not len(message.content) > 10:
            return

        make_ignore_channel_table(message.guild.id)

        ignore_channel_ids = ignore_channels_list(message.guild.id)

        if message.channel.id in ignore_channel_ids:
            return

        check_level_for_server_and_user(message.guild.id, message.author.id)

        cooldown_time = get_user_cooldown(message.guild.id, message.author.id)

        if cooldown_time >= int(time.time()):
            return

        increase_user_xp(message.guild.id, message.author.id)

        user_level, total_xp = get_user_level(message.guild.id, message.author.id)

        check_levelroles_for_server_role_and_level(message.guild.id)

        await level_roles_apply(message.guild, [[message.author.id, user_level]])


def setup(client):
    client.add_cog(LevelsGainXp(client))