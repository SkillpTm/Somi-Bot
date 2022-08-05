import nextcord
from nextcord import Embed
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone
import re

client = commands.Bot()

class ryujin_378214190378123264(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, ctx):
    user = await self.client.fetch_user("378214190378123264")
    if str(ctx.author.id) == "378214190378123264":
      return
    if ctx.author.bot:
      return
    if ctx.guild:
      if ctx.channel.id == 898969582608478209:
        return
      if ctx.channel.id == 562987593801793556:
        return
      if ctx.channel.id == 829872518717243432:
        return
      if ctx.channel.id == 829871264982106182:
        return
      if "ryujin" in re.sub(":.*?:", "", str(ctx.content.lower())):
        link = "https://discord.com/channels/" + str(ctx.guild.id) + "/" + str(ctx.channel.id) + "/" + str(ctx.id)
        embed = Embed(title="Keyword notification: `ryujin`",
                      colour=nextcord.Color.from_rgb(255, 166, 252))
        format = "%Y/%m/%d %H:%M:%S %Z"
        now_utc = datetime.now(timezone("UTC"))
        now_korea = now_utc.astimezone(timezone("Asia/Seoul"))
        embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
        if len(ctx.content) > 910:
          fields = [("Reason:", "Your keyword: `ryujin` has been said in <#" + str(ctx.channel.id) + "> by <@" + str(ctx.author.id) + ">:", False),
                    ("Message:", str(ctx.content[:910]) + "...  [Link](" + str(link) + ")", True)]
        else:
          fields = [("Reason:", "Your keyword: `ryujin` has been said in <#" + str(ctx.channel.id) + "> by <@" + str(ctx.author.id) + ">:", False),
                    ("Message:", str(ctx.content) + "  [Link](" + str(link) + ")", True)]
        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
        await user.send(embed=embed)
        if len(ctx.attachments) > 0:
          for i in range(len(ctx.attachments)):
            await user.send(ctx.attachments[i].url)

def setup(client):
  client.add_cog(ryujin_378214190378123264(client))