import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import time

from lib.modules import Checks, Get
from lib.utilities import SomiBot



class Ping(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "ping", description = "shows the bot's ping to discord")
    @nextcord_AC.check(Checks.interaction_not_by_bot())
    async def ping(self, interaction: nextcord.Interaction) -> None:
        """This command shows the ping and some general stats about the bot"""

        start = time.time()

        self.client.Loggers.action_log(Get.log_message(interaction, "/ping"))

        await interaction.response.send_message(content = f"DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`\n" + 
                                                          f"Up since = <t:{self.client.start_time}:R>")

        end = time.time()
        
        await interaction.edit_original_message(content = f"DWSP latency (ping) = `{self.client.latency * 1000:,.0f}ms`\n" + 
                                                          f"Response time: `{(end-start) * 1000 :,.0f}ms`\n" +
                                                          f"Up since = <t:{self.client.start_time}:R>")



def setup(client: SomiBot) -> None:
    client.add_cog(Ping(client))