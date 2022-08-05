import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class textresponse(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###somi###########################################################
  
  @nextcord.slash_command(name = "somi", description = "speaks facts")
  async def somi(self, interaction: Interaction):
    await interaction.response.send_message("Somi best grill https://i.imgur.com/65E2MWr.png")

  ###invite###########################################################

  @nextcord.slash_command(name = "invite", description = "Invites aren't open currently")
  async def invite(self, interaction: Interaction):
    await interaction.response.send_message("There currently isn't a way to invite this bot to another server and it isn't planned. For more information please message" + " <@" + str(378214190378123264) + ">", ephemeral=True)

  ###about###########################################################

  @nextcord.slash_command(name = "about", description = "Tells you about Somi bot")
  async def about(self, interaction: Interaction):
    await interaction.response.send_message("Somi#6418 is a themed bot after the kpop soloist Jeon Somi written in Python. Originally it was created to fullfil all needs of Somicord (https://discord.gg/Frd7WYg) and its subcords. The bot was created by Skillp#0309 and is currently in version 1.0. You can report bugs with /bugs and make suggestions with /suggestions!")

  ###levelroles###########################################################

  @nextcord.slash_command(name = "levelroles", description = "A list and explanation of level roles")
  async def modcommandlist(self, interaction: Interaction):
    embed = Embed(title="Level Roles",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("What are level roles?", "If you send a message you receive a few xp points. These xp points will eventually make you level up and at certain levels you get level roles.", False),
              ("Role list:", "Level 40-∞: <@&903568100291641384>\nLevel 30-39: <@&871898047146242099>\nLevel 20-29: <@&829886767125102614>\nLevel 10-19: <@&829886386386501652>\nLevel 3-9: <@&829885499828076624>", False),
              ("Perks:", "These level roles only give you a different color and put you higher on the members list. The only exception is: From your first level role on (<@&829885499828076624>) you will be allowed to send pictures/video, upload files and your links will have embeds.", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

def setup(client):
  client.add_cog(textresponse(client))