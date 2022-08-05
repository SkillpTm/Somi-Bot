import os
import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

client = commands.Bot()

class keywords(commands.Cog):

  def __init__(self, client):
    self.client = client

  from maincommands import keyword
    
  ###keyword#add###########################################################

  @keyword.subcommand(name = "add", description = "add a keyword to your keyword list")
  async def keyword_add(self, interaction: Interaction, *, keyword = SlashOption(description="Your new keyword", required=True)):
    interaction_user_keywords = []
    for filename in os.listdir("./keywords"):
      if filename.startswith(str(interaction.user.id)):
        head, sep, tail = filename.partition("_")
        interaction_user_keywords.append(tail[:-3])
    if keyword.lower().replace(" ", "") in interaction_user_keywords:
      await interaction.response.send_message("You already have `" + keyword.lower().replace(" ", "") + "` as a keyword.", ephemeral=True)
    else:
          keyword_add = open("./keywords/" + str(interaction.user.id) + "_" + keyword.lower().replace(" ", "") + ".py", "a")
          keyword_add.write('import nextcord\n' + 
                            'from nextcord import Embed\n' + 
                            'from nextcord.ext import commands\n' +
                            'from datetime import datetime\n' +
                            'from pytz import timezone\n' +
                            'import re\n\n' +
                            'client = commands.Bot()\n\n' +
                            'class ' + keyword.lower().replace(" ", "") + '_' + str(interaction.user.id) + '(commands.Cog):\n\n' +
                            '  def __init__(self, client):\n' +
                            '    self.client = client\n\n' +
                            '  @commands.Cog.listener()\n' +
                            '  async def on_message(self, ctx):\n' +
                            '    user = await self.client.fetch_user("' + str(interaction.user.id) + '")\n' +
                            '    if str(ctx.author.id) == "' + str(interaction.user.id) + '":\n' +
                            '      return\n' +
                            '    if ctx.author.bot:\n' +
                            '      return\n' +
                            '    if ctx.guild:\n' +
                            '      if ctx.channel.id == 898969582608478209:\n' +
                            '        return\n' +
                            '      if ctx.channel.id == 562987593801793556:\n' +
                            '        return\n' +
                            '      if ctx.channel.id == 829872518717243432:\n' +
                            '        return\n' +
                            '      if ctx.channel.id == 829871264982106182:\n' +
                            '        return\n' +
                            '      if ctx.channel.id == 980067444783730688:\n' +
                            '        return\n' +
                            '      if "' + keyword.lower().replace(" ", "") + '" in re.sub(":.*?:", "", str(ctx.content.lower())):\n' +
                            '        link = "https://discord.com/channels/" + str(ctx.guild.id) + "/" + str(ctx.channel.id) + "/" + str(ctx.id)\n' +
                            '        embed = Embed(title="Keyword notification: `' + keyword.lower().replace(" ", "") + '`",\n' +
                            '                        colour=nextcord.Color.from_rgb(255, 166, 252))\n' +
                            '        format = "%Y/%m/%d %H:%M:%S %Z"\n' +
                            '        now_utc = datetime.now(timezone("UTC"))\n' +
                            '        now_korea = now_utc.astimezone(timezone("Asia/Seoul"))\n' +
                            '        embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")\n' +
                            '        if len(ctx.content) > 910:\n'
                            '          fields = [("Reason:", "Your keyword: `' + keyword.lower().replace(" ", "") + '` has been said in <#" + str(ctx.channel.id) + "> by <@" + str(ctx.author.id) + ">:", False),\n' +
                            '                    ("Message:", str(ctx.content[:910]) + "...  [Link](" + str(link) + ")", True)]\n' +
                            '        else:\n' +
                            '          fields = [("Reason:", "Your keyword: `' + keyword.lower().replace(" ", "") + '` has been said in <#" + str(ctx.channel.id) + "> by <@" + str(ctx.author.id) + ">:", False),\n' +
                            '                    ("Message:", str(ctx.content) + "  [Link](" + str(link) + ")", True)]\n' +
                            '        for name, value, inline in fields:\n' +
                            '          embed.add_field(name=name, value=value, inline=inline)\n' +
                            '        await user.send(embed=embed)\n' +
                            '        if len(ctx.attachments) > 0:\n' +
                            '          for i in range(len(ctx.attachments)):\n' +
                            '            await user.send(ctx.attachments[i].url)\n\n' +
                            'def setup(client):\n' +
                            '  client.add_cog(' + keyword.lower().replace(" ", "") + '_' + str(interaction.user.id) + '(client))')
          keyword_add.close()
          await interaction.response.send_message("Your keyword new `" + keyword.lower().replace(" ", "") + "` has been added to your keyword list", ephemeral=True)
          for filename in os.listdir("./keywords"):
            if filename == str(interaction.user.id) + "_" + keyword.lower().replace(" ", "") + ".py":
                self.client.load_extension(f'keywords.{str(interaction.user.id) + "_" + keyword.lower().replace(" ", "")}')

  ###keyword#delete###########################################################

  @keyword.subcommand(name = "delete", description = "delete a keyword from your keyword list")
  async def keyword_delete(self, interaction: Interaction, *, keyword = SlashOption(description="The keyword to be deleted", required=True)):
    interaction_user_keywords = []
    for filename in os.listdir("./keywords"):
      if filename.startswith(str(interaction.user.id)):
        head, sep, tail = filename.partition("_")
        interaction_user_keywords.append(tail[:-3])
    if keyword.lower().replace(" ", "") in interaction_user_keywords:
      for filename in os.listdir("./keywords"):
        if filename == str(interaction.user.id) + "_" + keyword.lower().replace(" ", "") + ".py":
          self.client.unload_extension(f'keywords.{str(interaction.user.id) + "_" + keyword.lower().replace(" ", "")}')
      os.remove("./keywords/" + str(interaction.user.id) + "_" + keyword.lower().replace(" ", "") + ".py")
      await interaction.response.send_message("`" + keyword.lower().replace(" ", "") + "` has been removed from your keyword list.", ephemeral=True)
    else:
      await interaction.response.send_message("You don't have a keyword called `" + keyword.lower().replace(" ", "") + "`.", ephemeral=True)

  ###keyword#list###########################################################

  @keyword.subcommand(name = "list", description = "Shows you your keyword list")
  async def keyword_list(self, interaction: Interaction):
    interaction_user_keywords = []
    for filename in os.listdir("./keywords"):
      if filename.startswith(str(interaction.user.id)):
        head, sep, tail = filename.partition("_")
        interaction_user_keywords.append(tail[:-3])
    if interaction_user_keywords == "":
      await interaction.response.send_message("You don't have any keywords.", ephemeral=True)
    else:
      embed = Embed(title="Keyword list for " + str(interaction.user.name),
                    colour=nextcord.Color.from_rgb(255, 166, 252))
      format = "%Y/%m/%d %H:%M:%S %Z"
      now_utc = datetime.now(timezone('UTC'))
      now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
      embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
      if interaction.user.avatar is not None:
        embed.set_thumbnail(url=interaction.user.avatar)
      else:
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
      output = ""
      sorted_interaction_user_keywords = sorted(interaction_user_keywords)
      for i in range(len(sorted_interaction_user_keywords)):
        output += str(i + 1) + ". `" + sorted_interaction_user_keywords[i] + "`\n"
      fields = [("Keywords:", str(output), True)]
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
      await interaction.send(embed=embed, ephemeral=True)
    
def setup(client):
  client.add_cog(keywords(client))