import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Config, Logger
from lib.modules import SomiBot



class JoinLog(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    async def join_log(self, member: nextcord.Member) -> None:
        """A log that activates, when someone joins a server and a join log is set"""

        Logger().action_log(
            member,
            "join log",
            {"member": str(member.id)}
        )

        if not (join_log := member.guild.get_channel(int(await db.Server.JOIN_LOG.get(member.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            author = "Join Log",
            author_icon = member.display_avatar.url,
            footer = "Joined Discord:",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = member.created_at,
            fields = [
                EmbedField(
                    "ID:",
                    f"`{member.id}`",
                    False
                ),
                EmbedField(
                    "Username:",
                    member.name,
                    True
                ),
                EmbedField(
                    "Public Flags:",
                    ", ".join(flag.name for flag in member.public_flags.all()),
                    False
                )
            ]
        )

        await join_log.send(embed=embed) # type: ignore
        await db.Telemetry.AMOUNT.increment("join log")



def setup(client: SomiBot) -> None:
    client.add_cog(JoinLog(client))