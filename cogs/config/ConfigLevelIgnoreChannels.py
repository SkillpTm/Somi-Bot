import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import Lists, SomiBot



class ConfigLevelIgnoreChannels(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.config.subcommand(name="level-ignore-channels", description="deactivate/activate xp gain in a channel")
    async def config_level_ignore_channels(
        self,
        interaction: nextcord.Interaction,
        action: str = nextcord.SlashOption(
            description = "which action do you want to take",
            required = True,
            choices = ["Add", "Remove"]
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            description = "the channel to have (no) xp gain in",
            required = False,
            channel_types = Lists.TEXT_CHANNELS)
        ) -> None:
        """This command will deactivate/activate XP in the given channel."""

        channel = channel or interaction.channel

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/config level-ignore-channel",
            {"action": action, "channel": str(channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if action == "Add":
            if not await self._add_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} added: {channel.mention} as a level-ignore-channel."

        elif action == "Remove":
            if not await self._remove_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the level-ignore-channels."


        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = self.client.config.PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/config level-ignore-channels:",
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
        "adds or doesn't add the channel indicated by the output bool"

        if not (added := await (await DBHandler(self.client.database, server_id=interaction.guild.id).level_ignore_channel()).add(channel.id)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} is already a level-ignore-channel.\nTo get a list of all the level-ignore-channels use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been added to the level-ignore-channels.\nThere won't be any XP gain in there anymore."), ephemeral=True)
        return added

    ####################################################################################################

    async def _remove_channel(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        if not (deleted := await (await DBHandler(self.client.database, server_id=interaction.guild.id).hidden_channel()).delete(channel.id)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} isn't a level-ignore-channel.\nTo get a list of all the level-ignore-channels use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been removed from the level-ignore-channels.\n You can now earn XP there again."), ephemeral=True)
        return deleted



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelIgnoreChannels(client))