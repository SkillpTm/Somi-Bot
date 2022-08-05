import os
import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands
from datetime import datetime
from pytz import timezone
import sys

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

def restart_client(): 
  os.execv(sys.executable, ['python'] + sys.argv)

class custom(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###custom###########################################################
  
  @nextcord.slash_command(name = "custom", description = "create a custom command (the /c is added automatically)")
  @application_checks.has_any_role(587673639101661194)
  async def custom(self, interaction: Interaction, *, commandname = SlashOption(description="Future commandname", required=True), content = SlashOption(description="Output for command", required=True)):
    custom_commands = []
    for filename in os.listdir("./customcogs"):
      if filename.endswith(".py"):
        custom_commands.append(filename[:-3])
    if "c_" + commandname.lower().replace(" ", "") in custom_commands:
      await interaction.response.send_message("This command name is already being used, please try again.", ephemeral=True)
    else:
      commands = open("./customcogs/c_" + commandname.lower().replace(" ", "") + ".py", "a")
      commands.write("import nextcord\nfrom nextcord import Interaction\nfrom nextcord.ext import commands\n\n" +
                     "intents = nextcord.Intents.default()\nintents.members = True\n\n" +
                     "client = commands.Bot(intents=intents)\n\n" +
                     "class c_" + commandname.lower().replace(" ", "") + "(commands.Cog):\n\n" +
                     "  def __init__(self, client):\n    self.client = client\n\n" +
                     "  ###c " + commandname.lower().replace(" ", "") + "###########################################################\n\n" +
                     "  from maincommands import c\n\n" +
                     '  @c.subcommand(name = "' + commandname.lower().replace(" ", "") + '", description = "' + content[:99] + '")\n' +
                     "  async def c_" + commandname.lower().replace(" ", "") + "(self, interaction: Interaction):\n" +
                     '    await interaction.response.send_message("' + content + '")\n\n' +
                     "def setup(client):\n  client.add_cog(c_" + commandname.lower().replace(" ", "") + "(client))")
      commands.close()
      await interaction.response.send_message("Your custom command has been created!", ephemeral=True)
      
      audit_log = self.client.get_channel(829871264982106182)
      embed = Embed(colour=nextcord.Color.from_rgb(255, 166, 252))
      format = "%Y/%m/%d %H:%M:%S %Z"
      now_utc = datetime.now(timezone('UTC'))
      now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
      embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
      if interaction.user.avatar is not None:
        embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
      else:
        embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
      fields = [("/custom:", "<@" + str(interaction.user.id) + "> created: `/c " + commandname.lower().replace(" ", "") +"`", True)]
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

  @custom.error
  async def custom_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###delcustom###########################################################

  @nextcord.slash_command(name = "delcustom", description = "delete a custom command (the /c is added automatically)")
  @application_checks.has_any_role(587673639101661194)
  async def delcustom(self, interaction: Interaction, *, commandname = SlashOption(description="The custom command to be deleted", required=True)):
    custom_commands = []
    for filename in os.listdir("./customcogs"):
      if filename.endswith(".py"):
        custom_commands.append(filename[:-3])
    if "c_" + commandname.lower().replace(" ", "") in custom_commands:
      os.remove("./customcogs/c_" + commandname.lower().replace(" ", "") + ".py")
      await interaction.response.send_message("The command has been deleted.", ephemeral=True)

      audit_log = self.client.get_channel(829871264982106182)
      embed = Embed(colour=nextcord.Color.from_rgb(255, 166, 252))
      format = "%Y/%m/%d %H:%M:%S %Z"
      now_utc = datetime.now(timezone('UTC'))
      now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
      embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
      if interaction.user.avatar is not None:
        embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
      else:
        embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
      fields = [("/delcustom:", "<@" + str(interaction.user.id) + "> deleted: `/c " + commandname.lower().replace(" ", "") +"`", True)]
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
    else:
      await interaction.response.send_message("There is no command with this name.", ephemeral=True)

  @delcustom.error
  async def delcustom_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###customlist###########################################################

  @nextcord.slash_command(name = "customlist", description = "shows a list of all custom commands")
  async def customlist(self, interaction: Interaction):
    custom_commands = []
    output = ""
    for filename in os.listdir("./customcogs"):
      if filename.endswith(".py"):
        custom_commands.append(filename[:-3])
    sorted_custom_commands = sorted(custom_commands)
    for i in range(len(sorted_custom_commands)):
      output += "/" + sorted_custom_commands[i].replace("_", " ") + "\n"
    embed = Embed(title="All Custom Commands",
                  colour=nextcord.Color.from_rgb(255, 166, 252))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Commands:", str(output)[:-1], True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)
      
def setup(client):
  client.add_cog(custom(client))