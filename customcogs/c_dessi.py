import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_dessi(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c dessi###########################################################

  from maincommands import c

  @c.subcommand(name = "dessi", description = "dessi takes")
  async def c_dessi(self, interaction: Interaction):
    await interaction.response.send_message("**Case 1: Dessi spoiled herself again**\n- It's not that hard to not spoil yourself\n-------\n**Case 2: Dessi had another terrible opinion**\n- Nah your opinions are all worthless since you said 'bts live is shit'\n- Anyway I need another server where people have good opinions\n-------\n**Case 3: Dessi said something against aegyo**\n- After saying 'Insects cuter than idols confirmed' your opinion on what's cute and what isn't is worthless\n-------\n**Case 4: Dessi is cheating again**\n- The ushe")

def setup(client):
  client.add_cog(c_dessi(client))