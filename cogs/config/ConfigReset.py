import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Table
from lib.helpers import EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot, YesNoButtons



class ConfigReset(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(Commands().data["config reset"].name, Commands().data["config reset"].description)
    async def config_reset(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command resets the entire config for the bot in the server."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to reset your entire config for the bot. This includes: Custom Commands, the Default Role, Hidden Channels, Level Ignore Channels, Level Roles and Logs __**(this can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("Your config has **not** been reset!"), ephemeral=True)
            return

        data = typing.cast(dict[Table, int | str | None], {db.Server.DEFAULT_ROLE: None} | {log: None for log in db.Server.get_log_types()})
        await db.Server._.set(interaction.guild.id, data)
        await db.CustomCommand._.delete(where={db.CustomCommand.SERVER: interaction.guild.id})
        await db.HiddenChannel._.delete(where={db.HiddenChannel.SERVER: interaction.guild.id})
        await db.LevelIgnoreChannel._.delete(where={db.LevelIgnoreChannel.SERVER: interaction.guild.id})
        await db.LevelRole._.delete(where={db.LevelRole.SERVER: interaction.guild.id})

        await interaction.send(embed=EmbedFunctions().get_success_message("Your config has succesfully been reset!"), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigReset(client))