###package#import###############################################################################

import nextcord
import nextcord.ext.commands
import nextcord.ext.application_checks

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_levels_ignore import make_ignore_channel_table, ignore_channel
from utilities.maincommands import checks
from utilities.variables import MODERATOR_ID



class LevelsIgnore(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client: nextcord.ext.commands.Bot = client

    from utilities.maincommands import levels

    ###level#roles#add###########################################################

    @levels.subcommand(name = "ignore", description = "[MOD] deactivate/activate xp gain in a channel")
    @nextcord.ext.application_checks.has_permissions(manage_channels=True)
    async def levels_ignore(self,
                            interaction: nextcord.Interaction,
                            channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=[nextcord.ChannelType.text,
                                                                                                     nextcord.ChannelType.news,
                                                                                                     nextcord.ChannelType.forum,
                                                                                                     nextcord.ChannelType.public_thread,
                                                                                                     nextcord.ChannelType.news_thread,
                                                                                                     nextcord.ChannelType.private_thread], description="the channel to have (no) xp gain in", required=False)):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        if channel == None:
            channel = interaction.channel

        print(f"{interaction.user}: /levels ignore {channel.name}")

        make_ignore_channel_table(interaction.guild.id)

        added = ignore_channel(interaction.guild.id, channel.id)

        if added:
            await interaction.response.send_message(f"There will be no XP gain in {channel.mention} anymore!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You can now again earn XP in {channel.mention}!", ephemeral=True)

        uses_update("mod_command_uses", "levels ignore")

    @levels_ignore.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(LevelsIgnore(client))