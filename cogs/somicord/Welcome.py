import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Welcome(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def welcome(self, member: nextcord.Member) -> None:
        """welcomes a user on the server"""

        if member.guild.id != self.client.SOMICORD_ID:
            return

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            description = f"Hey {member.mention}, welcome to `{member.guild.name}`!\nWhat you waiting for - start chatting.",
            image = self.client.SOMICORD_WELCOME_GIF
        )
        sent_message = await member.guild.get_channel(self.client.SOMICORD_WELCOME_CHANNEL_ID).send(embed=embed)
        await sent_message.add_reaction(self.client.SOMI_WELCOME_EMOTE)



def setup(client: SomiBot) -> None:
    client.add_cog(Welcome(client))