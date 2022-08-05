###package#import###############################################################################

from datetime import datetime
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pytz import timezone

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class kst(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "kst", description = "shows the current time in KST")
    async def kst(self,
                  interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /kst")

        format = "Date: `%Y/%m/%d`\nTime: `%H:%M:%S %Z`"
        now_utc = datetime.now(timezone('UTC'))
        now_korea = now_utc.astimezone(timezone('Asia/Seoul'))

        await interaction.response.send_message(now_korea.strftime(format))

        uses_update("command_uses", "kst")

def setup(client):
    client.add_cog(kst(client))