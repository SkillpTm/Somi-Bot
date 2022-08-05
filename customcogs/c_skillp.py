import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_skillp(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c skillp###########################################################

  from maincommands import c

  @c.subcommand(name = "skillp", description = "skillp is amazing")
  async def c_skillp(self, interaction: Interaction):
    await interaction.response.send_message("skillp is amazing")

def setup(client):
  client.add_cog(c_skillp(client))