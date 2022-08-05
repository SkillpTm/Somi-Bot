import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_genericresponse(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c genericresponse###########################################################

  from maincommands import c

  @c.subcommand(name = "genericresponse", description = "happy for u or sorry that happened")
  async def c_genericresponse(self, interaction: Interaction):
    await interaction.response.send_message("happy for u or sorry that happened")

def setup(client):
  client.add_cog(c_genericresponse(client))