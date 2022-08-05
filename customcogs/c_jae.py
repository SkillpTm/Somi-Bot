import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_jae(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c jae###########################################################

  from maincommands import c

  @c.subcommand(name = "jae", description = "In case of an investigation by any federal entity or similar, I do not have any involvement with th")
  async def c_jae(self, interaction: Interaction):
    await interaction.response.send_message("In case of an investigation by any federal entity or similar, I do not have any involvement with this group or with the people in it, I do not know how I am here, probably added by a third party, I do not support any actions by the member of this group.")

def setup(client):
  client.add_cog(c_jae(client))