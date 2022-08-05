import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
import datetime
from datetime import datetime as timedate
from pytz import timezone


client = commands.Bot()

class link_embed(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###auto#link#embed###########################################################

  @commands.Cog.listener()
  async def on_message(self, interaction: Interaction):
    if str(interaction.author.id) == "939537452937412699":
      return
      
  ###reaction#on#ping###########################################################
      
    if self.client.user.mentioned_in(interaction):
      await interaction.add_reaction("<a:aSomiBreathTaking:980083399005982801>")
    if "https://discord.com/channels/" in str(interaction.content):
      head, sep, tail = interaction.content.partition("https")
      link = sep + tail
      head2, sep2, tail2 = link.partition(" ")
      only_link = head2
      head3, sep3, tail3 = only_link.partition("channels/")
      head4, sep4, tail4 = tail3.partition("/")
      head5, sep5, tail5 = tail4.partition("/")
      for channel in self.client.get_all_channels():
        try:
          msg = await channel.fetch_message(tail5)
          correct_channel = channel
        except:
          continue
      embed = Embed(description= "<#" + str(correct_channel.id) + "> - [Link](" + only_link + ")",
                    colour=nextcord.Color.from_rgb(255, 166, 252))
      if msg.author.avatar is not None:
        embed.set_author(name= "Message embed", icon_url=msg.author.avatar)
      else:
        embed.set_author(name= "Message embed", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
      format = "%Y/%m/%d %H:%M:%S %Z"
      now_utc = timedate.now(timezone("UTC"))
      now_korea = now_utc.astimezone(timezone("Asia/Seoul"))
      embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
      if msg.attachments:
        embed.set_image(url=msg.attachments[0].url)
      if msg.content == "":
        pass
      elif len(msg.content) > 970:
        fields = [(msg.author.name + " said:", msg.content[:970] + "...", False)]
        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
      else:
        fields = [(msg.author.name + " said:", msg.content, False)]
        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
      await interaction.reply(embed=embed)

def setup(client):
  client.add_cog(link_embed(client))