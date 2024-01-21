####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import TEXT_CHANNELS, SomiBot



class ConfigAuditLogChannel(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "audit-log-channel", description = "set/unset a channel for the bot to post logs")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def config_audit_log_channel(self,
                                       interaction: nextcord.Interaction,
                                       *,
                                       action: str = nextcord.SlashOption(description="which action do you want to take", required=True, choices=["Set", "Unset"]),
                                       channel: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=TEXT_CHANNELS, description="the channel to be set/unset", required=False)):
        """This command sets/unsets the audit-log-channel of the server."""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /config audit-log-channel {action}: {channel.id}")

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Set":
            added = ConfigDB(interaction.guild.id, "AuditLogChannel").add(channel.id)

            if not added:
                await interaction.followup.send(embed=EmbedFunctions().error(f"This server already has an audit-log-channel.\nUnset your audit-log-channel first."), ephemeral=True)
                return
                
            await interaction.followup.send(embed=EmbedFunctions().success(f"{channel.mention} is from now on this server's audit-log-channel."), ephemeral=True)

            audit_log_channel = channel
            mod_action = f"{interaction.user.mention} set: {channel.mention} as the new audit-log-channel."


        elif action == "Unset":
            channel_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)
            deleted = ConfigDB(interaction.guild.id, "AuditLogChannel").delete(channel.id)

            if not deleted:
                await interaction.followup.send(embed=EmbedFunctions().error("This server doesn't have an audit-log-channel."), ephemeral=True)
                return
            
            await interaction.followup.send(embed=EmbedFunctions().success("You successfully unset this server's audit-log-channel."), ephemeral=True)

            audit_log_channel = interaction.guild.get_channel(channel_id)
            mod_action = f"{interaction.user.mention} unset: <#{channel_id}> as the audit-log-channel."


        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config audit-log-channel:",
                    mod_action,
                    False
                ]
            ]
        )

        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(ConfigAuditLogChannel(client))