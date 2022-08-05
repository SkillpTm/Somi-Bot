import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_lol(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c lol###########################################################

  from maincommands import c

  @c.subcommand(name = "lol", description = "Kekekekekekekekekekekekekekekekekekekekekekekeke")
  async def c_lol(self, interaction: Interaction):
    await interaction.response.send_message("Kekekekekekekekekekekekekekekekekekekekekekekeke")

def setup(client):
  client.add_cog(c_lol(client))