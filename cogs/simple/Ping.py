####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import time

####################################################################################################

from lib.modules import Checks, Get
from lib.utilities import SomiBot



class Ping(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "ping", description = "shows the bot's ping to discord")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def ping(self,
                   interaction: nextcord.Interaction):
        """This command shows the ping and some general stats about the bot"""

        start = time.time()

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /ping")

        visible_users = Get().visible_users(self.client)

        await interaction.response.send_message(content = f"DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`" + 
                                                          f"\nUptime = <t:{self.client.start_time}:R>" + 
                                                          f"\nVisible Users: `{visible_users}`")

        end = time.time()
        
        await interaction.edit_original_message(content = f"DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`" + 
                                                          f"\nResponse time: `{(end-start) * 1000 :,.0f}ms`" +
                                                          f"\nUptime = <t:{self.client.start_time}:R>" +
                                                          f"\nVisible Users: `{visible_users}`")



def setup(client: SomiBot):
    client.add_cog(Ping(client))