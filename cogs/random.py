import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone
import random

client = commands.Bot()

class random_cog(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###ping###########################################################
  
  @nextcord.slash_command(name = "ping", description = "shows ping")
  async def ping(self, ctx):
    await ctx.send(f'ping = {round(self.client.latency * 1000)}ms')

  ###kst###########################################################

  @nextcord.slash_command(name = "kst", description = "shows the current time in KST")
  async def kst(self, interaction: Interaction):
    format = "Date: %Y/%m/%d\nTime: %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    await interaction.response.send_message(now_korea.strftime(format))
    
  ###coinflip###########################################################
  
  @nextcord.slash_command(name = "coinflip", description = "Does a coinflip")
  async def coinflip(self, interaction: Interaction):
    flip = random.randint(0, 1)
    if flip == 0:
      await interaction.response.send_message("Heads")
    if flip == 1:
      await interaction.response.send_message("Tails")

  ###emoji###########################################################

  @nextcord.slash_command(name="emoji", description="make an emoji larger")
  async def emoji(self, ctx, emoji):
    head, sep, tail = emoji[3:].partition(":")
    if emoji[1:].startswith("a"):
      emoji_url = "https://cdn.discordapp.com/emojis/" + tail[:-1] + ".gif"
      await ctx.send(emoji_url)
    elif emoji[1:].startswith(":") and emoji[1:].endswith(">"):
      emoji_url = "https://cdn.discordapp.com/emojis/" + tail[:-1] + ".webp"
      await ctx.send(emoji_url)
    else:
      await ctx.send("Please select an emoji.", ephemeral=True)

def setup(client):
  client.add_cog(random_cog(client))