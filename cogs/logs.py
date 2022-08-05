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
    if message.author.bot:
      return
    if message.channel.id == 898969582608478209:
      return
    elif message.channel.id == 562987593801793556:
      return
    elif message.channel.id == 829872518717243432:
      return
    elif message.channel.id == 829871264982106182:
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
    if message.content == "":
      pass
    elif len(message.content) > 970:
      embed.add_field(name = "Deleted message:", value = message.content[:970] + "...", inline = True)
    else:
      embed.add_field(name = "Deleted message:", value = message.content, inline = True)
    audit_log = self.client.get_channel(829871264982106182)
    await audit_log.send(embed=embed)
    if len(message.attachments) > 0:
      for i in range(len(message.attachments)):
        await audit_log.send(message.attachments[i].url)

  ###edit#log###########################################################

  @commands.Cog.listener()
  async def on_message_edit(self, message_before, message_after):
    if message_before.author.bot:
      return
    if message_before.channel.id == 898969582608478209:
      return
    elif message_before.channel.id == 562987593801793556:
      return
    elif message_before.channel.id == 829872518717243432:
      return
    elif message_before.channel.id == 829871264982106182:
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
    if message_after.content == "":
      pass
    elif len(message_before.content + message_after.content) > 970:
      fields = [("Before:", message_before.content[:485] + "...", False),
              ("After:", message_after.content[:485] + "...", False)]
    else:
      fields = [("Before:", message_before.content, False),
              ("After:", message_after.content, False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    audit_log = self.client.get_channel(829871264982106182)
    await audit_log.send(embed=embed)
    if len(message_before.attachments) > 0:
      for i in range(len(message_before.attachments)):
        await audit_log.send(message_before.attachments[i].url)

  ###name#log###########################################################

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    if before.bot:
      return
    if before == after and before.nick == after.nick:
      return
    if before != after:
      correct_before = before
      correct_after = after
      event = "Name ID"
    elif before.nick != after.nick:
      correct_before = before.nick
      correct_after = after.nick
      event = "Nickname"
    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(title=str(before) + " Changed Their " + event,
                  colour=Color.yellow())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = timedate.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if before.avatar is not None:
      embed.set_thumbnail(url=before.avatar)
    else:
      embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [(event + " before:", correct_before, False),
              (event + " after", correct_after, False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)
      
def setup(client):
  client.add_cog(entering_leaving(client))