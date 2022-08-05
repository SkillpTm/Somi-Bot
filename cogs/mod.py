import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands
from datetime import datetime
from datetime import timedelta
import humanfriendly
from pytz import timezone

intents = nextcord.Intents.all()

client = commands.Bot(intents=intents)

class mod(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###mute###########################################################

  @nextcord.slash_command(name="mute", description="mutes a user")
  @application_checks.has_any_role(587673639101661194)
  async def mute(self, ctx, *, target:nextcord.Member = SlashOption(description="The member to be muted", required=True), time = SlashOption(description="The time to mute the player for (input: xd or xh or xm or xs (x = whole positive number))", required=True), reason = SlashOption(description="Reason for the mute", required=False)):
    if target.id == 378214190378123264:
      await ctx.send("You can't mute Skillp!", ephemeral=True)
      return
    if ctx.user == target:
      await ctx.send("You can't mute yourself!", ephemeral=True)
      return
    time = humanfriendly.parse_timespan(time)
    await target.edit(timeout=nextcord.utils.utcnow()+timedelta(seconds=time))
    if reason != None:
      await ctx.send(f"<@" + str(target.id) + "> has been muted because: " + str(reason), ephemeral=True)
    else:
      await ctx.send(f"<@" + str(target.id) + "> has been muted", ephemeral=True)

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.yellow())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if ctx.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=ctx.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    if reason != None:
      fields = [("/mute:", "<@" + str(ctx.user.id) + "> muted: <@" + str(target.id) +"> for: `" + str(time) + "`\nBecause: " + str(reason), True)]
    else:
      fields = [("/mute:", "<@" + str(ctx.user.id) + "> muted: <@" + str(target.id) +"> for: `" + str(time) + "`", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  @mute.error
  async def mute_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###unmute###########################################################

  @nextcord.slash_command(name="unmute", description="unmutes a user")
  @application_checks.has_any_role(587673639101661194)
  async def unmute(self, ctx, *, target:nextcord.Member = SlashOption(description="Member to be unmuted", required=True)):
    await target.edit(timeout=None)
    await ctx.send(f"<@" + str(target.id) + "> has been unmuted", ephemeral=True)

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.green())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if ctx.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=ctx.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [("/unmute:", "<@" + str(ctx.user.id) + "> unmuted: <@" + str(target.id) +">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  @unmute.error
  async def unmute_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###purge###########################################################
    
  @nextcord.slash_command(name="purge", description="clears the entered amount of messages")
  @application_checks.has_any_role(587673639101661194)
  async def purge(self, ctx, *, amount: int = SlashOption(description="Amount of messages to be purged", required=True)):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Succesfully purged the last `" + str(amount) + "` messages from <#" + str(ctx.channel.id) + ">", ephemeral=True)

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.yellow())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if ctx.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=ctx.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    if amount == 1:
      fields = [("/purge:", "<@" + str(ctx.user.id) + "> purged: `" + str(amount) + " message` in <#" + str(ctx.channel.id) +">", True)]
    else:
      fields = [("/purge:", "<@" + str(ctx.user.id) + "> purged: `" + str(amount) + " messages` in <#" + str(ctx.channel.id) +">", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  @purge.error
  async def purge_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###kick###########################################################
    
  @nextcord.slash_command(name="kick", description="kicks a member")
  @application_checks.has_any_role(587673639101661194)
  async def kick(self, ctx, *, member: nextcord.Member = SlashOption(description="Member to be kicked", required=True), reason = SlashOption(description="Reason for the kick", required=False)):
    if member.id == 378214190378123264:
      await ctx.send("You can't kick Skillp!", ephemeral=True)
      return
    if ctx.user == member:
      await ctx.send("You can't kick yourself!", ephemeral=True)
      return
    await member.kick(reason=reason)
    if reason != None:
      await ctx.send("Succesfully kicked <@" + str(member.id) + "> because: " + str(reason), ephemeral=True)
      fields = [("/kick:", "<@" + str(ctx.user.id) + "> kicked: <@" + str(member.id) +">\nBecause: " + str(reason), True)]
    else:
      await ctx.send("Succesfully kicked <@" + str(member.id) + ">", ephemeral=True)
      fields = [("/kick:", "<@" + str(ctx.user.id) + "> kicked: <@" + str(member.id) +">", True)]

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.orange())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if ctx.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=ctx.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  @kick.error
  async def kick_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###ban###########################################################
    
  @nextcord.slash_command(name="ban", description="bans a member")
  @application_checks.has_any_role(587673639101661194)
  async def ban(self, ctx, *, member: nextcord.Member = SlashOption(description="Member to be banned", required=True), reason = SlashOption(description="Reason for the ban", required=False)):
    if member.id == 378214190378123264:
      await ctx.send("You can't ban Skillp!", ephemeral=True)
      return
    if ctx.user == member:
      await ctx.send("You can't ban yourself!", ephemeral=True)
      return
    await member.ban(reason=reason)
    if reason != None:
      await ctx.send("Succesfully banned <@" + str(member.id) + "> because: " + str(reason), ephemeral=True)
      fields = [("/ban:", "<@" + str(ctx.user.id) + "> banned: <@" + str(member.id) +">\nBecause: " + str(reason), True)]
    else:
      await ctx.send("Succesfully banned <@" + str(member.id) + ">", ephemeral=True)
      fields = [("/ban:", "<@" + str(ctx.user.id) + "> banned: <@" + str(member.id) +">", True)]

    audit_log = self.client.get_channel(829871264982106182)
    embed = Embed(colour=Color.red())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if ctx.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=ctx.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await audit_log.send(embed=embed)

  @ban.error
  async def ban_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###send###########################################################

  @nextcord.slash_command(name="send", description="sends a message in a channel")
  @application_checks.has_any_role(587673639101661194)
  async def send(self, interaction: Interaction, *, message = SlashOption(description="The message to be send by the bot", required=True), channel: nextcord.abc.GuildChannel = SlashOption(description="Channel in which the message will be send", required=False)):
    if channel == None:
      channel = interaction.channel
    message_id = await channel.send(message)
    await interaction.response.send_message("Message send in: <#" + str(channel.id) + ">", ephemeral=True)

    link = "https://discord.com/channels/" + str(interaction.guild.id) + "/" + str(channel.id) + "/" + str(message_id.id)
    embed = Embed(description= str(interaction.user.name) + " send a bot message in: <#" + str(channel.id) + "> " + "\n[Link](" + link + ")",
                  colour=Color.blue())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [("Message:", message, False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    audit_log = self.client.get_channel(829871264982106182)
    await audit_log.send(embed=embed)

  @send.error
  async def send_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###edit###########################################################

  @nextcord.slash_command(name="edit", description="edits a bot message in a channel")
  @application_checks.has_any_role(587673639101661194)
  async def edit(self, interaction: Interaction, *, message_id = SlashOption(description="ID of the message to be edited", required=True), message = SlashOption(description="The new message to be edited by the bot", required=True)):
    for channel in self.client.get_all_channels():
      try:
        msg = await channel.fetch_message(message_id)
        correct_channel = channel
      except:
        continue
    await msg.edit(content=message)
    await interaction.response.send_message("Message edited in: <#" + str(correct_channel.id) + ">", ephemeral=True)
    
    link = "https://discord.com/channels/" + str(interaction.guild.id) + "/" + str(correct_channel.id) + "/" + str(message_id)
    embed = Embed(description= str(interaction.user.name) + " edited a bot message in: <#" + str(correct_channel.id) + "> " + "\n[Link](" + link + ")",
                  colour=Color.blue())
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    if interaction.user.avatar is not None:
      embed.set_author(name= "Mod Activity", icon_url=interaction.user.avatar)
    else:
      embed.set_author(name= "Mod Activity", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    fields = [("New text:", message, False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    audit_log = self.client.get_channel(829871264982106182)
    await audit_log.send(embed=embed)

  @edit.error
  async def edit_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###close###########################################################

  @nextcord.slash_command(name="close", description="Takes regular users the sending message permission away.")
  @application_checks.has_any_role(587673639101661194)
  async def close(self, interaction: Interaction):
    sommungchi = interaction.guild.get_role(562728593663197194)
    permissions = nextcord.Permissions()
    permissions.update(send_messages = False, send_messages_in_threads = False, add_reactions = False, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True,  request_to_speak = True)
    await sommungchi.edit(permissions=permissions)
    await interaction.response.send_message("Closed the server sucessfully.", ephemeral=True)

  @close.error
  async def close_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###unclose###########################################################

  @nextcord.slash_command(name="unclose", description="Gives regular users the sending message permission.")
  @application_checks.has_any_role(587673639101661194)
  async def unclose(self, interaction: Interaction):
    sommungchi = interaction.guild.get_role(562728593663197194)
    permissions = nextcord.Permissions()
    permissions.update(send_messages = True, send_messages_in_threads = True, add_reactions = True, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True,  request_to_speak = True)
    await sommungchi.edit(permissions=permissions)
    await interaction.response.send_message("Re-opened the server sucessfully.", ephemeral=True)

  @unclose.error
  async def unclose_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)
    
  ###modcommandlist###########################################################

  @nextcord.slash_command(name = "modcommandlist", description = "A list of all mod commands")
  @application_checks.has_any_role(587673639101661194)
  async def modcommandlist(self, interaction: Interaction):
    embed = Embed(title="A list of all mod commands",
                        colour=nextcord.Color.from_rgb(255, 166, 252))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Commands:", "/ban\n/close\n/custom\n/delcustom\n/edit\n/kick\n/modcommandslist (alias: /mcl)\n/mute\n/purge\n/reload\n/restart\n/send\n/shutdown\n/unclose\n/unmute", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)

  @modcommandlist.error
  async def modcommandlist_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

  ###modcommandlist#alias###########################################################

  @nextcord.slash_command(name = "mcl", description = "A list of all mod commands (alias of /modcommandlist)")
  @application_checks.has_any_role(587673639101661194)
  async def mcl(self, interaction: Interaction):
    embed = Embed(title="A list of all mod commands",
                        colour=nextcord.Color.from_rgb(255, 166, 252))
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    embed.set_footer(text = now_korea.strftime(format), icon_url = "https://i.imgur.com/nqDFTTP.png")
    fields = [("Commands:", "/ban\n/close\n/custom\n/delcustom\n/edit\n/kick\n/modcommandslist (alias: /mcl)\n/mute\n/purge\n/reload\n/restart\n/send\n/shutdown\n/unclose\n/unmute", True)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await interaction.send(embed=embed, ephemeral=True)

  @mcl.error
  async def mcl_error(self, ctx, error):
    await ctx.send("Only <@&587673639101661194> can use this command", ephemeral=True)

def setup(client):
  client.add_cog(mod(client))