import os
import nextcord
from nextcord import Color, Embed, Interaction
from nextcord.ext import application_checks, commands
from datetime import datetime
from pytz import timezone
import sys
from webserver import keep_alive

intents = nextcord.Intents.all()

print(os.getenv("Somi"))
my_secret = os.environ['token']
client = commands.Bot(intents=intents)

###cog#import###############################################################################

for extension in os.listdir("./cogs/"):
  if extension.endswith(".py"):
    client.load_extension(f'cogs.{extension[:-3]}')

for extension in os.listdir("./customcogs/"):
  if extension.endswith(".py"):
    client.load_extension(f'customcogs.{extension[:-3]}')

for extension in os.listdir("./keywords/"):
  if extension.endswith(".py"):
    client.load_extension(f'keywords.{extension[:-3]}')

###restart###############################################################################

def restart_client(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.slash_command(name="restart", description="restarts the entire bot")
@application_checks.has_any_role(587673639101661194)
async def restart(interaction: Interaction):
  await interaction.response.send_message("Restarting bot...", ephemeral=True)

  audit_log = client.get_channel(829871264982106182)
  embed = Embed(colour=Color.blue())
  format = "%Y/%m/%d %H:%M:%S %Z"
  now_utc = datetime.now(timezone('UTC'))
  now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
  embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
  if interaction.user.avatar is not None:
    embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
  else:
    embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
  fields = [("/restart:", "<@" + str(interaction.user.id) + "> restarted the bot", True)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  await audit_log.send(embed=embed)

  embed = Embed(colour=Color.blue())
  format = "%Y/%m/%d %H:%M:%S %Z"
  now_utc = datetime.now(timezone('UTC'))
  now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
  embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
  embed.set_author(name= "Bot Activity", icon_url="https://cdn.discordapp.com/avatars/939537452937412699/6c7a6979391619341789363fbee3dfe5.png")
  fields = [("Shutdown", "The bot is about to shutdown", True)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  await audit_log.send(embed=embed)
  
  restart_client()

@restart.error
async def restart_error(ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

###reload###############################################################################
  
@client.slash_command(name="reload", description="reload the entire bot")
@application_checks.has_any_role(587673639101661194)
async def reload(interaction: Interaction):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      print(filename)
      client.reload_extension(f'cogs.{filename[:-3]}')
  for filename in os.listdir("./customcogs"):
    if filename.endswith(".py"):
      print(filename)
      client.reload_extension(f'customcogs.{filename[:-3]}')
  for filename in os.listdir("./keywords"):
    if filename.endswith(".py"):
      print(filename)
      client.reload_extension(f'keywords.{filename[:-3]}')
  await interaction.response.send_message("Bot has been reloaded", ephemeral=True)

  audit_log = client.get_channel(829871264982106182)
  embed = Embed(colour=Color.blue())
  format = "%Y/%m/%d %H:%M:%S %Z"
  now_utc = datetime.now(timezone('UTC'))
  now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
  embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
  if interaction.user.avatar is not None:
    embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
  else:
    embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
  fields = [("/reload:", "<@" + str(interaction.user.id) + "> reloaded the bot", True)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  await audit_log.send(embed=embed)

@reload.error
async def reload_error(ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

###on#ready###############################################################################

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

  await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='XOXO - The First Album'))
  
  audit_log = client.get_channel(829871264982106182)
  embed = Embed(colour=Color.blue())
  format = "%Y/%m/%d %H:%M:%S %Z"
  now_utc = datetime.now(timezone('UTC'))
  now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
  embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
  embed.set_author(name= "Bot Activity", icon_url="https://cdn.discordapp.com/avatars/939537452937412699/6c7a6979391619341789363fbee3dfe5.png")
  fields = [("Restarted", "The bot is back online", True)]
  for name, value, inline in fields:
    embed.add_field(name=name, value=value, inline=inline)
  await audit_log.send(embed=embed)

##################################################################################

keep_alive()
client.run(os.getenv('token'))