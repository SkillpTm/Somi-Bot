import nextcord
from nextcord import Color, Embed, Interaction
from nextcord.ext import commands
import datetime
from datetime import datetime as timedate
from pytz import timezone

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class entering_leaving(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###welcome#message###########################################################
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    role = nextcord.utils.get(member.guild.roles, id=562728593663197194)
    await member.add_roles(role)
    welcomechannel = self.client.get_channel(562717668285612135)
    await welcomechannel.send("Hey " + "<@" + str(member.id) + ">, welcome to Jeon Somi! What you waiting for - start chatting. \nhttps://gfycat.com/partialoblongfreshwatereel")

  ###join#log###########################################################
    
    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(title="New Member Joined:\n" + str(member),
                  colour=Color.green())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if member.avatar is not None:
      embed.set_thumbnail(url=member.avatar)
    else:
      embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    time1 = datetime.datetime.strptime(str(member.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    fields = [("ID:", member.id, False),
             ("Name:", member.mention, True),
             ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  ###leave#log###########################################################

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(title="Member Left:\n" + str(member),
                  colour=Color.red())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if member.avatar is not None:
      embed.set_thumbnail(url=member.avatar)
    else:
      embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    time1 = datetime.datetime.strptime(str(member.created_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time1 = datetime.datetime.timestamp(time1)
    time2 = datetime.datetime.strptime(str(member.joined_at.strftime("%m/%d/%Y %H:%M:%S")), "%m/%d/%Y %H:%M:%S")
    unix_time2 = datetime.datetime.timestamp(time2)
    fields = [("ID:", member.id, False),
              ("Name:", member.mention, True),
              ("Created at:", "<t:" + str(unix_time1)[:-2] + ">", True),
              ("Joined at",  "<t:" + str(unix_time2)[:-2] + ">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  ###delete#log###########################################################

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if str(message.author.id) == "939537452937412699":
      return
    if str(message.author.id) == "962494471902203965":
      return
    if str(message.author.id) == "283848369250500608":
      return
    if str(message.author.id) == "537353774205894676":
      return
    if str(message.author.id) == "325387620266016768":
      return
    if str(message.author.id) == "155149108183695360":
      return
    if str(message.author.id) == "204255221017214977":
      return
    embed = Embed(description= "Deleted in: <#" + str(message.channel.id) + ">",
                  colour=Color.red())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if message.author.avatar is not None:
      embed.set_author(name= str(message.author) + " deleted a message", icon_url=message.author.avatar)
    else:
      embed.set_author(name= str(message.author) + " deleted a message", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name = "Deleted message:", value = message.content, inline = True)
    channel = self.client.get_channel(829871264982106182)
    await channel.send(embed=embed)

  ###edit#log###########################################################

  @commands.Cog.listener()
  async def on_message_edit(self, message_before, message_after):
    if str(message_before.author.id) == "939537452937412699":
      return
    if str(message_before.author.id) == "962494471902203965":
      return
    if str(message_before.author.id) == "283848369250500608":
      return
    if str(message_before.author.id) == "537353774205894676":
      return
    if str(message_before.author.id) == "325387620266016768":
      return
    if str(message_before.author.id) == "155149108183695360":
      return
    if str(message_before.author.id) == "204255221017214977":
      return
    if message_before.content == message_after.content:
      return
    link = "https://discord.com/channels/" + str(message_before.guild.id) + "/" + str(message_before.channel.id) + "/" + str(message_before.id)
    embed = Embed(description= "Edited in: <#" + str(message_before.channel.id) + "> " + "[Link](" + link + ")",
                  colour=Color.yellow())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if message_before.author.avatar is not None:
      embed.set_author(name= str(message_before.author) + " edited a message", icon_url=message_before.author.avatar)
    else:
      embed.set_author(name= str(message_before.author) + " edited a message", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [("Before:", message_before.content, False),
              ("After:", message_after.content, False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    channel = self.client.get_channel(829871264982106182)
    await channel.send(embed=embed)

  ###auto#link#embed###########################################################

  @commands.Cog.listener()
  async def on_message(self, interaction: Interaction):
    if str(interaction.author.id) == "939537452937412699":
      return
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
                    colour=nextcord.Color.from_rgb(33, 233, 200))
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
  client.add_cog(entering_leaving(client))