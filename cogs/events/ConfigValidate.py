import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.modules import SomiBot



class ConfigValidate(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    async def on_delete(self, subject: nextcord.abc.GuildChannel | nextcord.Thread | nextcord.Role) -> None:
        """removes a channel/role from the Config, if it got deleted"""

        if isinstance(subject, nextcord.abc.GuildChannel) or isinstance(subject, nextcord.Thread):
            if subject.id == await db.Server.AUDIT_LOG.get(subject.guild.id):
                await db.Server.AUDIT_LOG.set(subject.guild.id, None)

            if await db.HiddenChannel._.get_entry(subject.id):
                await db.HiddenChannel._.delete(subject.id)

            if await db.LevelIgnoreChannel._.get_entry(subject.id):
                await db.LevelIgnoreChannel._.delete(subject.id)

        elif isinstance(subject, nextcord.Role):
            if subject.id == await db.Server.DEFAULT_ROLE.get(subject.guild.id):
                await db.Server.DEFAULT_ROLE.set(subject.guild.id, None)

            if await db.LevelRole._.get_entry(subject.id):
                await db.LevelRole._.delete(subject.id)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigValidate(client))