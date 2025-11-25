import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot, YesNoButtons



class ConfigLevelIgnoreChannels(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(
        Commands().data["config level-ignore-channels"].alias,
        Commands().data["config level-ignore-channels"].description,
        name_localizations = {country_tag: Commands().data["config level-ignore-channels"].name for country_tag in nextcord.Locale}
    )
    async def config_level_ignore_channels(
        self,
        interaction: nextcord.Interaction[SomiBot],
        action: typing.Literal["Add", "Remove", "Remove All"] = nextcord.SlashOption(
            Commands().data["config level-ignore-channels"].parameters["action"].name,
            Commands().data["config level-ignore-channels"].parameters["action"].description,
            required = True,
            choices = ["Add", "Remove", "Remove All"]
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["config level-ignore-channels"].parameters["channel"].name,
            Commands().data["config level-ignore-channels"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS)
        ) -> None:
        """This command will deactivate/activate XP in the given channel."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        channel = channel or interaction.channel

        if action == "Add":
            if not await self._add_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} added: {channel.mention} as a level-ignore-channel."

        elif action == "Remove":
            if not await self._remove_channel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the level-ignore-channels."

        elif action == "Remove All":
            if not await self.remove_all(interaction):
                return

            mod_action = f"{interaction.user.mention} removed **ALL** level-ignore-channels."


        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config level-ignore-channels"].name}:",
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
        "adds or doesn't add the channel indicated by the output bool"

        if not (added := await db.LevelIgnoreChannel._.add({db.LevelIgnoreChannel.ID: channel.id, db.LevelIgnoreChannel.SERVER: interaction.guild.id})):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} is already a level-ignore-channel.\nTo get a list of all the level-ignore-channels use `/config info`."))
            return added

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been added to the level-ignore-channels.\nThere won't be any XP gain in there anymore."))
        return added


    async def _remove_channel(
        self,
        interaction: nextcord.Interaction[SomiBot],
        channel: nextcord.TextChannel | nextcord.Thread
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        if not (deleted := await db.LevelIgnoreChannel._.delete(interaction.guild.id, channel.id)):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{channel.mention} isn't a level-ignore-channel.\nTo get a list of all the level-ignore-channels use `/config info`."), ephemeral=True)
            return deleted

        await interaction.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} has been removed from the level-ignore-channels.\n You can now earn XP there again."), ephemeral=True)
        return deleted


    async def remove_all(self, interaction: nextcord.Interaction[SomiBot]) -> bool:
        """Removes all level-ignore-channels after user confirmation."""

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to remove **ALL** your level-ignore-channels __**(they can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("Your level-ignore-channels have **not** been removed!"))
            return False

        await db.LevelIgnoreChannel._.delete(where={db.LevelIgnoreChannel.SERVER: interaction.guild.id}, limit=1_000_000)

        return True



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLevelIgnoreChannels(client))