import nextcord
from nextcord import Color, Embed, Interaction
from nextcord.ext import application_checks, commands
from datetime import datetime
from pytz import timezone

client = commands.Bot()

class Question(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout = 20)
    self.value = None

  @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green) #blurple, green, red, gray
  async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message("Bot is being shutdown", delete_after=20, ephemeral=True) #False=everyone can see the text, true=only this user can see the text
    self.value = True
    self.stop()

  @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red) #dblurple, green, red, gray
  async def no(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message("Bot has not been shutdown", delete_after=20, ephemeral=True) #False=everyone can see the text, true=only this user can see the text
    self.value = False
    self.stop()

class shutdown(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###shutdown###########################################################
  
  @nextcord.slash_command(name = "shutdown", description = "Shutdown the bot immeaditly")
  @application_checks.has_any_role(587673639101661194)
  async def shutdown(self, interaction: Interaction):
    view = Question()
    await interaction.response.send_message("Do you really want to shutdown the bot?", view=view, ephemeral=True, delete_after=20)
    await view.wait()

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.orange())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [("/shutdown:", "<@" + str(interaction.user.id) + "> shutdown the bot", True)]
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

    if view.value is None:
      return

    elif view.value:
      await self.client.close()

    else:
      print("Bot did not shutdown")

  @shutdown.error
  async def shutdown_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

def setup(client):
  client.add_cog(shutdown(client))