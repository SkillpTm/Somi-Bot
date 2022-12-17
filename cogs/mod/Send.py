###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR



class Send(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###send###########################################################

    @nextcord.slash_command(name="send", description="[MOD] sends a message in a channel")
    @nextcord.ext.application_checks.has_permissions(manage_messages=True)
    async def send(self,
                   interaction: nextcord.Interaction,
                   *,
                   message: str = nextcord.SlashOption(description="the message to be send by the bot", required=True, min_length=1, max_length=1000),
                   channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=[nextcord.ChannelType.text,
                                                                                            nextcord.ChannelType.news,
                                                                                            nextcord.ChannelType.forum,
                                                                                            nextcord.ChannelType.public_thread,
                                                                                            nextcord.ChannelType.news_thread,
                                                                                            nextcord.ChannelType.private_thread], description="channel in which the message will be send", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        if channel == None:
            channel = interaction.channel

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        print(f"{interaction.user}: /send {message} {channel}")

        message_object = await channel.send(message)
        await interaction.response.send_message(f"Message sent in: {channel.mention} - [Link]({message_object.jump_url})", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(description = f"{interaction.user.mention} sent a bot message in: {channel.mention} - [Link]({message_object.jump_url})",
            	              color = MOD_COLOR,
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Message:",
                              field_one_value = message,
                              field_one_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "send")

    @send.error
    async def send_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

    ###edit###########################################################

    @nextcord.slash_command(name="edit", description="[MOD] edits a bot message in a channel")
    @nextcord.ext.application_checks.has_permissions(manage_messages=True)
    async def edit(self,
                   interaction: nextcord.Interaction,
                   *,
                   message_id: str = nextcord.SlashOption(description="ID of the message to be edited", required=True, min_length=18, max_length=19),
                   message: str = nextcord.SlashOption(description="the new message to be edited by the bot", required=True, min_length=1, max_length=1000)):
        if not checks(interaction.guild, interaction.user):
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        for channel in await interaction.guild.fetch_channels():
            msg = ""
            try:
                msg = await channel.fetch_message(int(message_id))
                correct_channel = channel
                break
            except:
                pass

        if msg == "" or msg.author.id != self.client.user.id:
            await interaction.response.send_message(f"`{message_id}` isn't an id of a message sent by the bot in this server!", ephemeral=True)
            return

        print(f"{interaction.user}: /edit {message_id}\nBefore: {msg.content}\nAfter: {message}")

        await msg.edit(content=message)
        
        await interaction.response.send_message(f"Message edited in: {correct_channel.mention} - [Link]({msg.jump_url})", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(description = f"{interaction.user.mention} edited a bot message in: {correct_channel.mention} - [Link]({msg.jump_url})",
            	              color = MOD_COLOR,
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Before:",
                              field_one_value = msg.content,
                              field_one_inline = False,
                              
                              field_two_name = "After:",
                              field_two_value = message,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "edit")

    @edit.error
    async def edit_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Send(client))