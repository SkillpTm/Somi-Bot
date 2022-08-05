import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
from datetime import datetime as timedate
import datetime
from typing import Optional
from pytz import timezone

intents = nextcord.Intents.all()

client = commands.Bot(intents=intents)

class info(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###userinfo###########################################################

  @nextcord.slash_command(name="userinfo", description = "gives information about a user")
  async def userinfo(self, interaction: Interaction, target: nextcord.Member):
    if target == None:
      target = interaction.user
    embed = Embed(title="User Information",
                  colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if target.avatar is not None:
      embed.set_thumbnail(url=target.avatar)
    else:
      embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    time1 = datetime.datetime.strptime(str(target.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    time2 = datetime.datetime.strptime(str(target.joined_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time2 = datetime.datetime.timestamp(time2)
    fields = [("ID", target.id, False),
              ("Name:", str(target), True),
              ("Top role", target.top_role.mention, True),
              ("Status", target.status, True),
              ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True),
              ("Joined at:", "<t:" + str(unix_time2)[:-2] + ">", True),
              ("Boosted", bool(target.premium_since), True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  ###userinfo#alias###########################################################

  @nextcord.slash_command(name="ui", description = "gives information about a user (alias of /userinfo)")
  async def ui(self, interaction: Interaction, target: nextcord.Member):
    if target == None:
      target = interaction.user
    embed = Embed(title="User Information",
                  colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if target.avatar is not None:
      embed.set_thumbnail(url=target.avatar)
    else:
      embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    time1 = datetime.datetime.strptime(str(target.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    time2 = datetime.datetime.strptime(str(target.joined_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time2 = datetime.datetime.timestamp(time2)
    fields = [("ID:", target.id, False),
              ("Name:", str(target), True),
              ("Top role:", target.top_role.mention, True),
              ("Status:", target.status, True),
              ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True),
              ("Joined at:", "<t:" + str(unix_time2)[:-2] + ">", True),
              ("Boosted:", bool(target.premium_since), True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  ###serverinfo###########################################################
    
  @nextcord.slash_command(name="serverinfo", description = "gives information about this server")
  async def serverinfo(self, interaction: Interaction):
    embed = Embed(title="Server Information",
                  colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.guild.icon is not None:
      embed.set_thumbnail(url=interaction.guild.icon)
    time1 = datetime.datetime.strptime(str(interaction.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    fields = [("ID:", interaction.guild.id, False),
              ("Members:", len(interaction.guild.members), True),
              ("Owner:", interaction.guild.owner, True),
              ("Channels:", str(len(interaction.guild.text_channels)) + " text, " + str(len(interaction.guild.voice_channels)) + " voice", True),
              ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  ###serverinfo#alias###########################################################
    
  @nextcord.slash_command(name="si", description = "gives information about this server (alias of /serverinfo)")
  async def si(self, interaction: Interaction):
    embed = Embed(title="Server Information:\n" + str(interaction.guild),
                  colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.guild.icon is not None:
      embed.set_thumbnail(url=interaction.guild.icon)
    time1 = datetime.datetime.strptime(str(interaction.guild.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    fields = [("ID:", interaction.guild.id, False),
              ("Members:", len(interaction.guild.members), True),
              ("Owner:", interaction.guild.owner, True),
              ("Channels:", str(len(interaction.guild.text_channels)) + " text, " + str(len(interaction.guild.voice_channels)) + " voice", True),
              ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  ###avatar###########################################################

  @nextcord.slash_command(name="avatar", description = "posts someone's avatar")
  async def avatar(self, interaction: Interaction, target: Optional[nextcord.Member]):
    if target == None:
      target = interaction.user
    embed = Embed(colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if str(target)[:-5][-1] == 's':
      embed.title= str(target)[:-5] + "' Avatar"
    else:
      embed.title= str(target)[:-5] + "'s Avatar"
    if target.avatar is not None:
      embed.set_image(url=target.avatar)
    else:
      embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    await interaction.send(embed=embed) 

def setup(client):
  client.add_cog(info(client))