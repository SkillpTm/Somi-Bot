import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_bvndit(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c bvndit###########################################################

  from maincommands import c

  @c.subcommand(name = "bvndit", description = "Call me old fashioned but I was born to serve BVNDIT. I was taught to wash their clothes, cook thei")
  async def c_bvndit(self, interaction: Interaction):
    await interaction.response.send_message("Call me old fashioned but I was born to serve BVNDIT. I was taught to wash their clothes, cook their meals, be ready for any task they assigned me and be honored that I get to serve them. If they cheat on me, that's on me. They caught me slipping.")

def setup(client):
  client.add_cog(c_bvndit(client))