###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_forbidden_channels
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID



class Slowmode(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###slowmode###########################################################
        
    @nextcord.slash_command(name="slowmode", description="[MOD] activates slowmode in a channel")
    @nextcord.ext.application_checks.has_permissions(manage_channels=True)
    async def slowmode(self,
                       interaction: nextcord.Interaction,
                       *,
                       delay: int = nextcord.SlashOption(description="how long it takes until a user can send a message again in seconds. (To end slowmode input '0')", required=True, min_value = 0, max_value = 3600),
                       channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=[nextcord.ChannelType.text,
                                                                                                nextcord.ChannelType.news,
                                                                                                nextcord.ChannelType.forum,
                                                                                                nextcord.ChannelType.public_thread,
                                                                                                nextcord.ChannelType.news_thread,
                                                                                                nextcord.ChannelType.private_thread], description="the channel to activate slowmode in", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        if channel == None:
            channel = interaction.channel

        if not checks_forbidden_channels(channel):
            await interaction.response.send_message("You can't activate slowmode in this channel.", ephemeral=True)
            return

        print(f"{interaction.user}: /slowmode {delay} {channel}")

        await channel.edit(slowmode_delay=delay)

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        member_avatar_url = get_user_avatar(interaction.user)

        if not delay == 0:
            await interaction.response.send_message(f"Activated slowmode in {channel.mention} with a delay of `{delay} seconds`.", ephemeral=True)
            field_value = f"{interaction.user.mention} activated slowmode in {channel.mention} with a delay of `{delay} seconds`"
        else:
            await interaction.response.send_message(f"Deactivated slowmode in {channel.mention}", ephemeral=True)
            field_value = f"{interaction.user.mention} deactivated slowmode in {channel.mention}"

        embed = embed_builder(color = nextcord.Color.orange(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/slowmode:",
                              field_one_value = field_value,
                              field_one_inline = False)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "slowmode")

    @slowmode.error
    async def slowmode_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Slowmode(client))