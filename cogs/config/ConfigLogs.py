import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Table
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot



class ConfigLogs(nextcord_C.Cog):

    log_types = {"All": db.Server._,} | {log.name.replace('_', ' ').title(): log for log in db.Server.get_log_types()}

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(Commands().data["config logs"].name, Commands().data["config logs"].description)
    async def config_logs(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        log_type: str = nextcord.SlashOption(
            Commands().data["config logs"].parameters["log_type"].name,
            Commands().data["config logs"].parameters["log_type"].description,
            required = True,
            choices = log_types.keys()
        ),
        action: typing.Literal["Set", "Reset"] = nextcord.SlashOption(
            Commands().data["config logs"].parameters["action"].name,
            Commands().data["config logs"].parameters["action"].description,
            required = True,
            choices = ["Set", "Reset"]
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["config logs"].parameters["channel"].name,
            Commands().data["config logs"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
    ) -> None:
        """This command sets/resets the logs of the server."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        channel = channel or interaction.channel
        data: dict[Table, int | str | None] | int | str | None

        if action == "Set":
            if not self.log_types[log_type].value:
                data = {val: channel.id for val in self.log_types.values() if val.value}
                response = f"You successfully set **all** this server's logs in {channel.mention}."
                mod_action = f"{interaction.user.mention} {action.lower()}: **all** this server's logs in {channel.mention}."
            else:
                data = channel.id
                response = f"You successfully set this server's `{log_type}` channel in {channel.mention}."
                mod_action = f"{interaction.user.mention} {action.lower()}: {channel.mention} as the `{log_type}` channel."

        elif action == "Reset":
            if not self.log_types[log_type].value:
                await self.reset_all(log_type, action, interaction)
                return

            if not (channel_id := int(await self.log_types[log_type].get(interaction.guild.id) or 0)):
                await interaction.send(embed=EmbedFunctions().get_error_message(f"This server has no `{log_type}` to reset."))
                return

            channel = typing.cast(nextcord.TextChannel | nextcord.Thread | None, interaction.guild.get_channel(channel_id)) or channel

            data = None
            response = f"You successfully reset this server's `{log_type}` channel."
            mod_action = f"{interaction.user.mention} {action.lower()}: <#{channel_id}> as the `{log_type}` channel."

        await self.log_types[log_type].set(interaction.guild.id, data)
        await interaction.send(embed=EmbedFunctions().get_success_message(response))

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = log_type if self.log_types[log_type].value else "All Logs",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config logs"].full_name}:",
                    mod_action,
                    False
                )
            ]
        )

        await channel.send(embed=embed)


    async def reset_all(self, log_type: str, action: str, interaction: nextcord.Interaction[SomiBot]) -> None:
        """Resets all log channels for the server."""

        channels: dict[int, list[str]] = {}
        types_log = {v.value: k for k, v in self.log_types.items()}

        for key, val in typing.cast(dict[str, int], await db.Server._.get_entry(interaction.guild.id)).items():
            if key not in types_log.keys() or not val or not interaction.guild.get_channel(val):
                continue

            if not channels.get(val):
                channels[val] = []

            channels[val].append(types_log[key])

        if not channels:
            await interaction.send(embed=EmbedFunctions().get_error_message("This server has no log channels to reset."))
            return

        await self.log_types[log_type].set(interaction.guild.id, {val: None for val in self.log_types.values() if val.value})
        await interaction.send(embed=EmbedFunctions().get_success_message("You successfully reset **all** this server's logs."))

        for channel_id, log_names in channels.items():
            channel = interaction.guild.get_channel(channel_id)

            embed = EmbedFunctions().builder(
                color = Config().PERMISSION_COLOR,
                author = "All Logs",
                author_icon = interaction.user.display_avatar.url,
                fields = [
                    EmbedField(
                        f"/{Commands().data["config logs"].full_name}:",
                        f"{interaction.user.mention} {action.lower()}: **all** this server's log channels. Logs previously in this channel:\n" +
                        ", ".join(f"`{log_name}`" for log_name in log_names),
                        False
                    )
                ]
            )

            await channel.send(embed=embed) #type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigLogs(client))