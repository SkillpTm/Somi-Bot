import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class c_dynamite(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###c dynamite###########################################################

  from maincommands import c

  @c.subcommand(name = "dynamite", description = "DYNAMITE ISN’T JUST A SONG, IT’S A CULTURAL RESET, IT’S THE OXYGEN YOU BREATHE, IT’S A LIFESTYLE, A")
  async def c_dynamite(self, interaction: Interaction):
    await interaction.response.send_message("DYNAMITE ISN’T JUST A SONG, IT’S A CULTURAL RESET, IT’S THE OXYGEN YOU BREATHE, IT’S A LIFESTYLE, A REASON TO BREATHE, AN ESCAPE FROM THIS CRUEL WORLD, IT’S ART, THE FIRST GIFT YOU OPEN ON CHRISTMAS, A HUG FROM A LOVED ONE, EVERYTHING YOU’VE EVER WANTED")

def setup(client):
  client.add_cog(c_dynamite(client))