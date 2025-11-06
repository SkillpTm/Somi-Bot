import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, SomiBot



class ConfigHiddenChannels(nextcord_C.Cog):

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
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            channel_types = Lists.TEXT_CHANNELS,
            description = "the channel to be added/removed",
            required = False)
        ) -> None:
        """This command adds a custom command to the server's custom commands"""

        channel = channel or interaction.channel

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/config hidden-channels",
            {"action": action, "channel": str(channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if action == "Add":
            if not await self._add_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} added: {channel.mention} as a hidden-channel."

        elif action == "Remove":
            if not await self._remove_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the hidden-channels."


        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = self.client.config.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/config hidden-channels:",
                    mod_action,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

    ####################################################################################################

    async def _add_channel(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not (added := await (await DBHandler(self.client.database, server_id=interaction.guild.id).hidden_channel()).add(channel.id)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} is already a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been added to the hidden-channels."), ephemeral=True)
        return added

    ####################################################################################################

    async def _remove_channel(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        if not (deleted := await (await DBHandler(self.client.database, server_id=interaction.guild.id).hidden_channel()).delete(channel.id)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} isn't a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been removed from the hidden-channels."), ephemeral=True)
        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigHiddenChannels(client))