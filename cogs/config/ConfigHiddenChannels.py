import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot, YesNoButtons



class ConfigHiddenChannels(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(Commands().data["config hidden-channels"].name, Commands().data["config hidden-channels"].description)
    async def config_hidden_channels(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        action: typing.Literal["Add", "Remove", "Remove All"] = nextcord.SlashOption(
            Commands().data["config hidden-channels"].parameters["action"].name,
            Commands().data["config hidden-channels"].parameters["action"].description,
            required = True,
            choices = ["Add", "Remove", "Remove All"]
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["config hidden-channels"].parameters["channel"].name,
            Commands().data["config hidden-channels"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
        ) -> None:
        """This command adds a custom command to the server's custom commands"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        channel = channel or interaction.channel

        if action == "Add":
            if not await self._add_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} added: {channel.mention} as a hidden-channel."

        elif action == "Remove":
            if not await self._remove_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the hidden-channels."

        elif action == "Remove All":
            if not await self.remove_all(interaction):
                return

            mod_action = f"{interaction.user.mention} removed **ALL** hidden-channels."


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config hidden-channels"].name}:",
                    mod_action,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    async def _add_channel(
        self,
        interaction: nextcord.Interaction[SomiBot],
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        if not (added := await db.HiddenChannel._.add({db.HiddenChannel.ID: channel.id, db.HiddenChannel.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} is already a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."))
            return added

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been added to the hidden-channels."))
        return added


    async def _remove_channel(
        self,
        interaction: nextcord.Interaction[SomiBot],
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        if not (deleted := await db.HiddenChannel._.delete({db.HiddenChannel.ID: channel.id, db.HiddenChannel.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} isn't a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."))
            return deleted

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been removed from the hidden-channels."))
        return deleted


    async def remove_all(self, interaction: nextcord.Interaction[SomiBot]) -> bool:
        """Removes all hidden-channels after user confirmation."""

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to remove **ALL** your hidden-channels __**(they can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("Your hidden-channels have **not** been removed!"))
            return False

        await db.HiddenChannel._.delete(where={db.HiddenChannel.SERVER: interaction.guild.id}, limit=1_000_000)

        return True



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigHiddenChannels(client))