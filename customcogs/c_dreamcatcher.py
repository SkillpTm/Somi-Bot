import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_dreamcatcher(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c dreamcatcher###########################################################

  from maincommands import c

  @c.subcommand(name = "dreamcatcher", description = "Dreamcatcher is the standard. The epitomy of musical excellence. The greatest performers of the cen")
  async def c_dreamcatcher(self, interaction: Interaction):
    await interaction.response.send_message("Dreamcatcher is the standard. The epitomy of musical excellence. The greatest performers of the century. History books, sculptures, paintings and every single medium of art need to have Dreamcatcher.")

def setup(client):
  client.add_cog(c_dreamcatcher(client))