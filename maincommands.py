import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

@client.slash_command(name='c', description='custom command')
async def c(interaction: Interaction):
  pass

@client.slash_command(name='help', description='Explanation for singular commands')
async def help(interaction: Interaction):
  pass

@client.slash_command(name='keyword', description='Gives notifications for selected keywords')
async def keyword(interaction: Interaction):
  pass

@client.slash_command(name='reminders', description="Let's you manage your remidners")
async def reminders(interaction: Interaction):
  pass