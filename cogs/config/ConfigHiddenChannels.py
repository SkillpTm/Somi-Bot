import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, SomiBot



class ConfigHiddenChannels(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="hidden-channels", description="add/remove a hidden-channel to this server")
    async def config_hidden_channels(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Add", "Remove"]
        ),
        channel: nextcord.abc.GuildChannel = nextcord.SlashOption(
            channel_types = Lists.TEXT_CHANNELS,
            description = "the channel to be added/removed",
            required = False)
        ) -> None:
        """This command adds a custom command to the server's custom commands"""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/config hidden-channels",
            {"action": action, "channel": str(channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Add":
            if not await self._addChannel(interaction, channel):
                return
            
            mod_action = f"{interaction.user.mention} added: {channel.mention} as a hidden-channel."   

        elif action == "Remove":
            if not await self._removeChannel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the hidden-channels."  


        audit_log_id = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).server()).audit_log_get()

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config hidden-channels:",
                    mod_action,
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

    ####################################################################################################

    async def _addChannel(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.abc.GuildChannel
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        added = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).hidden_channel()).add(channel.id)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} is already a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been added to the hidden-channels."), ephemeral=True)
        return added

    ####################################################################################################

    async def _removeChannel(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.abc.GuildChannel
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        deleted = await (await DBHandler(self.client.PostgresDB, server_id=interaction.guild.id).hidden_channel()).delete(channel.id)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} isn't a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been removed from the hidden-channels."), ephemeral=True)
        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigHiddenChannels(client))