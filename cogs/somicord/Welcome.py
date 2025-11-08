import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Config
from lib.utilities import SomiBot



class Welcome(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def welcome(self, member: nextcord.Member) -> None:
        """welcomes a user on the server"""

        if member.guild.id != Config().MODMAIL_SERVER_ID:
            return

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            description = f"Hey {member.mention}, welcome to `{member.guild.name}`!\nWhat you waiting for - start chatting.",
            image = Config().SOMICORD_WELCOME_GIF
        )

        sent_message = await member.guild.get_channel(Config().WELCOME_CHANNEL_ID).send(embed=embed)
        await sent_message.add_reaction(Config().SOMI_WELCOME_EMOTE)



def setup(client: SomiBot) -> None:
    client.add_cog(Welcome(client))