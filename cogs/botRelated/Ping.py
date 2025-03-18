import nextcord
import nextcord.ext.commands as nextcord_C
import subprocess
import time

from lib.dbModules import DBHandler
from lib.modules import Get
from lib.utilities import SomiBot



class Ping(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="ping", description="shows the bot's ping to discord")
    async def ping(self, interaction: nextcord.Interaction) -> None:
        """This command shows the ping and some general stats about the bot"""

        defer_start = time.time()

        self.client.Loggers.action_log(Get.log_message(interaction, "/ping"))

        await interaction.response.defer(with_message=True)

        defer_end = time.time()

        followup_start = time.time()

        await interaction.followup.send(content="🏓 Pong!")

        followup_end = time.time()

        cpu_usage = round(float(subprocess.run("top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'", shell=True, capture_output=True, text=True).stdout.strip()), 1)
        mem_usage = round(float(subprocess.run("top -bn1 | grep 'MiB Mem' | awk '{print 100 - ((($6 + $10)/$4) * 100)}'", shell=True, capture_output=True, text=True).stdout.strip()), 1)

        await interaction.followup.edit_message(
            message_id = (await interaction.original_message()).id,
            content =
                f"Pong!🏓\n" +
                f"Up since: <t:{self.client.start_time}:R>\n" +
                f"Discord latency: `{round(self.client.latency * 1000)}ms`\n" +
                f"Response time: `{round((defer_end-defer_start) * 1000)}ms`\n" +
                f"Followup time: `{round((followup_end-followup_start) * 1000)}ms`\n" +
                f"Database latency: `{await DBHandler(self.client.PostgresDB).get_latency()}ms`\n" +
                f"CPU usage: `{cpu_usage}%`\n" +
                f"RAM usage: `{mem_usage}%`\n"
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Ping(client))