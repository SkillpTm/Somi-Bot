import nextcord
from nextcord import Color, Embed, Interaction, DMChannel
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

intents = nextcord.Intents.all()

client = commands.Bot(intents=intents)

class modmail(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###modmail###########################################################

  @commands.Cog.listener()
  async def on_message(self, message):
    mod_channel = self.client.get_channel(980074784626982972)
    if isinstance(message.channel, DMChannel):
      if not message.author.bot:
        if len(message.content) < 50:
          await message.channel.send("Your modmail must be longer than 50 characters!")
        else:
          embed = Embed(title="Modmail by " + str(message.author),
                        colour=Color.blue())
          format = "%Y/%m/%d %H:%M:%S %Z"
          now_utc = datetime.now(timezone('UTC'))
          now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
          embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
          if message.author.avatar is not None:
            embed.set_thumbnail(url=message.author.avatar)
          else:
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
          if len(message.content) > 940:
            fields = [("ID:", message.author.id, True),
                      ("Member:", " <@" + str(message.author.id) + ">", True),
                      ("Message:", message.content[:940], False)]
          else:
            fields = [("ID:", message.author.id, True),
                      ("Member:", " <@" + str(message.author.id) + ">", True),
                      ("Message:", message.content, False)]
          for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
          if len(message.attachments) > 0:
            for i in range(len(message.attachments)):
              await mod_channel.send(message.attachments[i].url)
          await mod_channel.send(embed=embed)
          await message.channel.send("Your modmail has been submitted!")          

def setup(client):
  client.add_cog(modmail(client))