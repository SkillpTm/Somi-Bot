import random
import re

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import LevelRoles
from lib.modules import SomiBot



class LevelsGainXp(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    async def levels_gain_xp(self, message: nextcord.Message) -> None:
        """This command gives xp to a user on the server the message was send, if the message:
            1. is longer than 10 characters
            2. was not send in a levels ignore channel
            3. was send after the user's cooldown went off

            afterwards the command will try to apply levelroles"""

        if not message.guild:
            return

        # re removes emotes, make sure messages are above 10 chars
        if not len(re.sub("<[^ ]+?>", "",message.content)) > 10:
            return

        if await db.HiddenChannel._.get_entry(message.channel.id):
            return

        entry = await db.Level._.get_entry({db.Level.SERVER: message.guild.id, db.Level.USER: message.author.id})

        if not entry:
            await db.Level._.add({db.Level.SERVER: message.guild.id, db.Level.USER: message.author.id})
            entry = await db.Level._.get_entry({db.Level.SERVER: message.guild.id, db.Level.USER: message.author.id})

        if db.Level.COOLDOWN.retrieve(entry) > int(message.created_at.timestamp()):
            return

        if not await db.Level._.set(
            {
                db.Level.SERVER: message.guild.id,
                db.Level.USER: message.author.id
            },
            {
                db.Level.COOLDOWN: int(message.created_at.timestamp()) + random.randint(55, 65),
                db.Level.XP: (new_total := db.Level.XP.retrieve(entry) + random.randint(10, 15))
            }
            ):
            return

        if db.Level._.get_level(db.Level.XP.retrieve(entry)) < db.Level._.get_level(new_total):
            await LevelRoles.update_users(message.guild, [{db.Level.USER: message.author.id, db.Level.XP: new_total}])



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsGainXp(client))