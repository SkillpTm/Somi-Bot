import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

client = commands.Bot()

class command_overview(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###commandlist###########################################################

  @nextcord.slash_command(name = "commandlist", description = "A list of all main commands")
  async def commandlist(self, interaction: Interaction):
    embed = Embed(title="A list of all main commands",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Commands:", "/about\n/avatar\n/bugs\n/c [custom name]\n/coinflip\n/commandlist (alias: /cl)\n/customlist\n/emoji\n/help [command name]\n/invite\n/keyword add\n/keyword delete\n/keyword list\n/kst\n/levelroles\n/ping\n/serverinfo (alias: /si)\n/somi\n/suggestions\n/userinfo (alias: ui)", True),
              ("Help:", "Explanations for singular commands can be found by typing '/help [command name]'", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)

  ###commandlist#alias###########################################################

  @nextcord.slash_command(name = "cl", description = "A list of all main commands")
  async def cl(self, interaction: Interaction):
    embed = Embed(title="A list of all commands",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Commands:", "/about\n/avatar\n/bugs\n/c [custom name]\n/coinflip\n/commandlist (alias: /cl)\n/customlist\n/emoji\n/help [command name]\n/invite\n/keyword add\n/keyword delete\n/keyword list\n/kst\n/levelroles\n/ping\n/serverinfo (alias: /si)\n/somi\n/suggestions\n/userinfo (alias: ui)", True),
              ("Help:", "Explanations for singular commands can be found by typing '/help [command name]'", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)

  ###help###########################################################

  from maincommands import help

  #####about#####

  @help.subcommand(name = "about", description = "help for 'about'")
  async def help_about(self, interaction: Interaction):
    embed = Embed(title="Help for /about",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/about (no parameters)", False),
              ("Info:", "This command will tell you everything you need to know about the current state of Somi#6418.\nIf you continue to require help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####avatar#####

  @help.subcommand(name = "avatar", description = "help for 'avatar'")
  async def help_avatar(self, interaction: Interaction):
    embed = Embed(title="Help for /avatar",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/avatar optional[@username]", False),
              ("Info:","This command will post the avatar of the selected user/you.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####bugs#####

  @help.subcommand(name = "bugs", description = "help for 'bugs'")
  async def help_bugs(self, interaction: Interaction):
    embed = Embed(title="Help for /bugs",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/bugs [text]", False),
              ("Info:","This command is meant to report bugs/typos/other issues you have encountered while using the bot. Be aware that, if you use this command your bug report, together with your ID and name will be stored in a file, until the problem is solved. You can add that you want to be informed, as soon as the problem has been fixed.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####c#####

  @help.subcommand(name = "c", description = "help for 'c'")
  async def help_c(self, interaction: Interaction):
    embed = Embed(title="Help for /c",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/c [custom name]", False),
              ("Info:","This command is a main command to several custom commands. All of these custom commands have been created by the moderators and can only be added/reomved by a moderator.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####coinflip#####

  @help.subcommand(name = "coinflip", description = "help for 'coinflip'")
  async def help_coinflip(self, interaction: Interaction):
    embed = Embed(title="Help for /coinflip",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/coinflip (no parameters)", False),
              ("Info:","This command gives out either heads or tails.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####commandlist#####

  @help.subcommand(name = "commandlist", description = "help for 'commandlist'")
  async def help_commandlist(self, interaction: Interaction):
    embed = Embed(title="Help for /commandlist",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/commandlist (no parameters)", False),
              ("Info:","This command outputs a list with all regular commands.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####cl#####

  @help.subcommand(name = "cl", description = "help for 'cl'")
  async def help_cl(self, interaction: Interaction):
    embed = Embed(title="Help for /cl",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/cl (no parameters)", False),
              ("Info:","This command outputs a list with all regular commands. (Alias of /commandlist)\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####emoji#####

  @help.subcommand(name = "emoji", description = "help for 'emoji'")
  async def help_emoji(self, interaction: Interaction):
    embed = Embed(title="Help for /emoji",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/emoji [emoji]", False),
              ("Info:","This command posts an emoji in it's original size.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####help#####

  @help.subcommand(name = "help", description = "help for 'help'")
  async def help_help(self, interaction: Interaction):
    embed = Embed(title="Help for /help",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/help [command name] or 'all'", False),
              ("Info:","This command gives you an explanation for what a certain command does.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####invite#####

  @help.subcommand(name = "invite", description = "help for 'invite'")
  async def help_invite(self, interaction: Interaction):
    embed = Embed(title="Help for /invite",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "invite (no parameters)", False),
              ("Info:","This command will tell you about our current invite policy.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####keyword#####

  @help.subcommand(name = "keyword", description = "help for 'keyword'")
  async def help_keyword(self, interaction: Interaction):
    embed = Embed(title="Help for /keyword",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/keyword add [keyword] or delete [keyword] or list", False),
              ("Info:","This command let's you add or delete a keyword to your keyword list, which you can open as well. If you set a keyword the bot will send you a direct message when someone else mentions this keyword.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####kst#####

  @help.subcommand(name = "kst", description = "help for 'kst'")
  async def help_kst(self, interaction: Interaction):
    embed = Embed(title="Help for /kst",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/kst (no parameters)", False),
              ("Info:","This command tells you the current time in KST (Korean Standard Time).\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####levelroles#####

  @help.subcommand(name = "levelroles", description = "help for 'levelroles'")
  async def help_levelroles(self, interaction: Interaction):
    embed = Embed(title="Help for /levelroles",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/levelroles (no parameters)", False),
              ("Info:","This command will explain the level system of this server to you. It also includes a list of all roles with levels.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####ping#####

  @help.subcommand(name = "ping", description = "help for 'ping'")
  async def help_ping(self, interaction: Interaction):
    embed = Embed(title="Help for /ping",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/ping (no parameters)", False),
              ("Info:","This command shows you the bot's current ping.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####serverinfo#####

  @help.subcommand(name = "serverinfo", description = "help for 'serverinfo'")
  async def help_serverinfo(self, interaction: Interaction):
    embed = Embed(title="Help for /serverinfo",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/serverinfo (no parameters)", False),
              ("Info:","This command gives you information about the server.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####si#####

  @help.subcommand(name = "si", description = "help for 'si'")
  async def help_si(self, interaction: Interaction):
    embed = Embed(title="Help for /si",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/si (no parameters)", False),
              ("Info:","This command gives you information about the server. (Alias of /serverinfo)\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####somi#####

  @help.subcommand(name = "somi", description = "help for 'somi'")
  async def help_somi(self, interaction: Interaction):
    embed = Embed(title="Help for /somi",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/somi (no parameters)", False),
              ("Info:","This command will tell you the truth and the truth only.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####suggestions#####

  @help.subcommand(name = "suggestions", description = "help for 'suggestions'")
  async def help_suggestions(self, interaction: Interaction):
    embed = Embed(title="Help for /suggestions",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/suggestions [Text]", False),
              ("Info:","This command is meant to give suggestions for the bot. Be aware that, if you use this command your suggestion, together with your ID and name will be stored in a file, until it has been approved/rejected. You can add that you want to be informed, about what is going to happen regrading your suggestion.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####userinfo#####

  @help.subcommand(name = "userinfo", description = "help for 'userinfo'")
  async def help_userinfo(self, interaction: Interaction):
    embed = Embed(title="Help for /userinfo",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/userinfo optional[@username]", False),
              ("Info:","This command will post the user information of the selected user/you.\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####ui#####

  @help.subcommand(name = "ui", description = "help for 'ui'")
  async def help_ui(self, interaction: Interaction):
    embed = Embed(title="Help for /ui",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Syntax:", "/ui optional[@username]", False),
              ("Info:","This command will post the user information of the selected user/you. (Alias of /userinfo)\nIf you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed)

  #####all#####

  @help.subcommand(name = "all", description = "help for all commands")
  async def help_all(self, interaction: Interaction):
    embed = Embed(title="Help for all commands",
                        colour=nextcord.Color.from_rgb(33, 233, 200))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("/about", "Syntax: /about (no parameters)\nInfo: This command will tell you everything you need to know about the current state of Somi#6418.", False),
              ("/avatar", "Syntax: /avatar optional[@username]\nInfo: This command will post the avatar of the selected user/you.", False),
              ("/bugs", "Syntax: /bugs [text]\nInfo: This command is meant to report bugs/typos/other issues you have encountered while using the bot. Be aware that, if you use this command your bug report, together with your ID and name will be stored in a file, until the problem is solved. You can add that you want to be informed, as soon as the problem has been fixed.", False),
              ("/c", "Syntax: /c [custom name]\nInfo: This command is a main command to several custom commands. All of these custom commands have been created by the moderators and can only be added/reomved by a moderator.", False),
              ("/coinflip", "Syntax: /coinflip (no parameters\nInfo: This command gives out either heads or tails.", False),
              ("/commandlist or /cl", "Syntax: /commandlist (no parameters)\nInfo: This command outputs a list with all regular commands.", False),
              ("/emoji", "Syntax: /emoji [emoji]\nInfo: This command posts an emoji in it's original size.", False),
              ("/help", "Syntax: /help [command name] or 'all'\nInfo: This command gives you an explanation for what a certain command does.", False),
              ("/invite", "Syntax: invite (no parameters)\nInfo: This command will tell you about our current invite policy.", False),
              ("/levelroles", "Syntax: /levelroles (no parameters)\nInfo: This command will explain the level system of this server to you. It also includes a list of all roles with levels.", False),
              ("/keyword:", "Syntax: /keyword add [keyword] or delete [keyword] or list\nInfo: This command let's you add or delete a keyword to your keyword list, which you can open as well. If you set a keyword the bot will send you a direct message when someone else mentions this keyword.", False),
              ("/kst", "Syntax: /kst (no parameters)\nInfo: This command tells you the current time in KST (Korean Standard Time).", False),
              ("/ping", "Syntax: /ping (no parameters)\nInfo: This command shows you the bot's current ping.", False),
              ("/severinfo or /si", "Syntax: /serverinfo (no parameters)\nInfo: This command gives you information about the server.", False),
              ("/somi", "Syntax: /somi (no parameters)\nInfo: This command will tell you the truth and the truth only.", False),
              ("/suggestions", "Syntax: /suggestion [Text]\nInfo: This command is meant to give suggestions for the bot. Be aware that, if you use this command your suggestion, together with your ID and name will be stored in a file, until it has been approved/rejected. You can add that you want to be informed, about what is going to happen regrading your suggestion.", False),
              ("/userinfo or /ui", "Syntax: /userinfo optional[@username]\nInfo: This command will post the user information of the selected user/you.", False),
              ("Further help:", "If you continue to require further help please message" + " <@" + str(378214190378123264) + ">", False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)

def setup(client):
  client.add_cog(command_overview(client))