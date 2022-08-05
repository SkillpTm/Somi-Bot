import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

intents = nextcord.Intents.all()

client = commands.Bot(intents = intents)

class roles(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  async def handle_click(self, button: nextcord.ui.button, interaction: Interaction):
    role_id, sep, tail = button.custom_id.partition(".")
    role = interaction.guild.get_role(int(role_id))
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.send_message("The role: <@&" + str(role_id) + "> has been removed form your role list", ephemeral=True)
    else:
      await interaction.user.add_roles(role)
      await interaction.response.send_message("The role: <@&" + str(role_id) + "> has been added to your role list", ephemeral=True)
      

  @nextcord.ui.button(label = "UPDATES", style=nextcord.ButtonStyle.blurple, custom_id="981654656457510953.UPDATES")
  async def UPDATES(self, button: nextcord.ui.Button, interaction: Interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label = "SNS", style=nextcord.ButtonStyle.blurple, custom_id="981655771156721735.SNS")
  async def SNS(self, button: nextcord.ui.Button, interaction: Interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label = "LIVE", style=nextcord.ButtonStyle.blurple, custom_id="981655862907138128.LIVE")
  async def LIVE(self, button: nextcord.ui.Button, interaction: Interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label = "ROLES", style=nextcord.ButtonStyle.gray, custom_id="Somi.ROLES")
  async def ROLES(self, button: nextcord.ui.Button, interaction: Interaction):
    rolelist = []
    rolelist = [i.mention for i in interaction.user.roles if i != interaction.guild.default_role]
    embed = Embed(colour=nextcord.Color.from_rgb(255, 166, 252))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.user.avatar is not None:
      embed.set_author(name= "Rolelist of " + str(interaction.user), icon_url=interaction.user.avatar)
    else:
      embed.set_author(name= "Rolelist of " + str(interaction.user), icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    output = ""
    for i in range(len(rolelist)):
      output += str(i + 1) + ". " + str(rolelist[i]) + "\n"
    fields = [("Roles:", str(output), True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)
    

class role_selection(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###roleselection#generation###########################################################
    
  @commands.Cog.listener()
  async def on_ready(self):
    roles_channel = self.client.get_channel(987692984864768041)
    messages = await roles_channel.history(limit=100).flatten()
    if messages == []:
      embed = Embed(title="Role selection",
                    colour=nextcord.Color.from_rgb(255, 166, 252))
      fields = [("Info Roles", "Info roles will ping you for a certain event. The currtent info roles are:\n<@&981654656457510953>: Informs you about big news (like a comeback).\n<@&981655771156721735>: Informs you about a SNS update.\n<@&981655862907138128>: Informs you about a live from Somi.", False),
                ("How It Works", 'Click the button of the role you want down below. If you want to get rid of a role afterwards just click the button again. If you are unsure about your current roles press the button "ROLES".', False)]
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
      await roles_channel.send(embed=embed, view=roles())
    else:
      return

def setup(client):
  client.add_cog(role_selection(client))