import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_rosé(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c rosé###########################################################

  from maincommands import c

  @c.subcommand(name = "rosé", description = "Rosé 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭💔💔💔💔💔😣😣😣💓💓💔💔💔💔💓😭 Rosé 😩😣 park roseanne 😔😔 RO SÉ 😔😔 ROSÉ <3 !!!!!!!!!! r o s é")
  async def c_rosé(self, interaction: Interaction):
    await interaction.response.send_message("Rosé 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭💔💔💔💔💔😣😣😣💓💓💔💔💔💔💓😭 Rosé 😩😣 park roseanne 😔😔 RO SÉ 😔😔 ROSÉ <3 !!!!!!!!!! r o s é 💔💔💔💔😭😭😭😭 rosé rosé. ROSÉ . 😭😭😭😭💔💓💓💓 Rosé rosééééé 💔😭😭😭😭 rosé!!!! Roseanne park 😭😣💔💔 hello ROSÉÉÉÉÉ i love you😭😭💔")

def setup(client):
  client.add_cog(c_rosé(client))