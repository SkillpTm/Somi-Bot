import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_objection(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c objection###########################################################

  from maincommands import c

  @c.subcommand(name = "objection", description = "isn't there that thing")
  async def c_objection(self, interaction: Interaction):
    await interaction.response.send_message("isn't there that thing")

def setup(client):
  client.add_cog(c_objection(client))