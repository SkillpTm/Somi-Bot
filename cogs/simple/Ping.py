###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.GlobalData import start_time
from database.database_command_uses import uses_update
from utilities.maincommands import checks



class Ping(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###ping###########################################################

    @nextcord.slash_command(name = "ping", description = "shows the bot's ping to discord")
    async def ping(self,
                   interaction: nextcord.Interaction):
        start = time.time()
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /ping")

        await interaction.response.send_message(f"""ping = `{self.client.latency * 1000:,.0f}ms`
        uptime = <t:{start_time}:R>
        Visible Users: `{len(self.client.users)}`""")

        end = time.time()
        
        await interaction.edit_original_message(f"""DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`
        Response time: `{(end-start) * 1000 :,.0f}ms`
        Uptime = <t:{start_time}:R>
        Visible Users: `{len(self.client.users)}`""")

        uses_update("command_uses", "ping")



def setup(client):
    client.add_cog(Ping(client))