import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, SomiBot



class ConfigAuditLogChannel(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="audit-log-channel", description="set/reset a channel for the bot to post logs")
    async def config_audit_log_channel(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Set", "Reset"]
        ),
        channel: nextcord.abc.GuildChannel = nextcord.SlashOption(
            description = "the channel to be set/reset",
            required = False,
            channel_types = Lists.TEXT_CHANNELS
        )
    ) -> None:
        """This command sets/resets the audit-log-channel of the server."""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/config audit-log-channel",
            {"action": action, "channel": str(channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Set":
            await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_set(channel.id)
            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} is from now on this server's audit-log-channel."), ephemeral=True)

            mod_action = f"{interaction.user.mention} set: {channel.mention} as the new audit-log-channel."

        elif action == "Reset":
            if not await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_reset():
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("This server doesn't have an audit-log-channel."), ephemeral=True)
                return
            
            await interaction.followup.send(embed=EmbedFunctions().get_success_message("You successfully reset this server's audit-log-channel."), ephemeral=True)

            mod_action = f"{interaction.user.mention} reset: {channel.mention} as the audit-log-channel."


        embed = EmbedFunctions().builder(
            color = self.client.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config audit-log-channel:",
                    mod_action,
                    False
                ]
            ]
        )

        await channel.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigAuditLogChannel(client))