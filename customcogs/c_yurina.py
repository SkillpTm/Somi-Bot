import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_yurina(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c yurina###########################################################

  from maincommands import c

  @c.subcommand(name = "yurina", description = "I need this so much!! Yurina is my one pick, my favorite idol, my shining star! You have no idea ho")
  async def c_yurina(self, interaction: Interaction):
    await interaction.response.send_message("I need this so much!! Yurina is my one pick, my favorite idol, my shining star! You have no idea how much I needed this in my life and I will support her so hard!! I love Yurina so much!! 😭🥳💕")

def setup(client):
  client.add_cog(c_yurina(client))