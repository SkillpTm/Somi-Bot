import subprocess
import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import Database
from lib.managers import Commands
from lib.modules import SomiBot



class Ping(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["ping"].name,
        Commands().data["ping"].description,
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def ping(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command shows the ping and some general stats about the bot"""

        start = time.perf_counter()

        await interaction.send(content="Pong! 🏓")

        end = time.perf_counter()

        cpu_usage = round(float(subprocess.run("top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'", shell=True, check=False, capture_output=True, text=True).stdout.strip().replace(",", ".")), 1)
        mem_usage = round(float(subprocess.run("top -bn1 | grep 'MiB Mem' | awk '{print 100 - ((($6 + $10)/$4) * 100)}'", shell=True, check=False, capture_output=True, text=True).stdout.strip().replace(",", ".")), 1)

        await interaction.followup.edit_message(
            message_id = (await interaction.original_message()).id,
            content =
                "Pong! 🏓\n" +
                f"Up since: <t:{self.client.start_time}:R>\n" +
                f"Discord latency: `{round(self.client.latency * 1000)}ms`\n" +
                f"Response time: `{round((end-start) * 1000)}ms`\n" +
                f"Database latency: `{await Database().get_latency()}ms`\n" +
                f"CPU usage: `{cpu_usage}%`\n" +
                f"RAM usage: `{mem_usage}%`\n"
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Ping(client))