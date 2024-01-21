####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import TEXT_CHANNELS, SomiBot



class ConfigHiddenChannels(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "hidden-channels", description = "add/remove a hidden-channel to this server")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def config_hidden_channels(self,
                                     interaction: nextcord.Interaction,
                                     *,
                                     action: str = nextcord.SlashOption(description="which action do you want to take", required=True, choices=["Add", "Remove"]),
                                     channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=TEXT_CHANNELS, description="the channel to be added/removed", required=False)):
        """This command adds a custom command to the server's custom commands"""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /config hidden-channels {action}: {channel.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Add":
            added = ConfigDB(interaction.guild.id, "HiddenChannels").add(channel.id)

            if not added:
                await interaction.followup.send(embed=EmbedFunctions().error(f"{channel.mention} is already a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
                return

            await interaction.followup.send(embed=EmbedFunctions().success(f"{channel.mention} has been added to the hidden-channels."), ephemeral=True)
        
            mod_action = f"{interaction.user.mention} added: {channel.mention} as a hidden-channel."   


        elif action == "Remove":
            deleted = ConfigDB(interaction.guild.id, "HiddenChannels").delete(channel.id)

            if not deleted:
                await interaction.followup.send(embed=EmbedFunctions().error(f"{channel.mention} isn't a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
                return

            await interaction.followup.send(embed=EmbedFunctions().success(f"{channel.mention} has been removed from the hidden-channels."), ephemeral=True)

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the hidden-channels."  


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config default-role:",
                    mod_action,
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(ConfigHiddenChannels(client))