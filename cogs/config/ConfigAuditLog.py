import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot



class ConfigAuditLog(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.config.subcommand(Commands().data["config audit-log"].name, Commands().data["config audit-log"].description)
    async def config_audit_log(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        action: typing.Literal["Set", "Reset"] = nextcord.SlashOption(
            Commands().data["config audit-log"].parameters["action"].name,
            Commands().data["config audit-log"].parameters["action"].description,
            required = True,
            choices = ["Set", "Reset"]
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["config audit-log"].parameters["channel"].name,
            Commands().data["config audit-log"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
    ) -> None:
        """This command sets/resets the audit-log of the server."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        channel = channel or interaction.channel

        if action == "Set":
            await db.Server.AUDIT_LOG.set(interaction.guild.id, channel.id)
            await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"{channel.mention} is from now on this server's audit-log-channel."), ephemeral=True)

            mod_action = f"{interaction.user.mention} set: {channel.mention} as the new audit-log-channel."

        elif action == "Reset":
            if not await db.Server.AUDIT_LOG.get(interaction.guild.id):
                await interaction.followup.send(embed=EmbedFunctions().get_error_message("This server doesn't have an audit-log-channel."), ephemeral=True)
                return

            await db.Server.AUDIT_LOG.set(interaction.guild.id, None)
            await interaction.followup.send(embed=EmbedFunctions().get_success_message("You successfully reset this server's audit-log-channel."), ephemeral=True)

            mod_action = f"{interaction.user.mention} reset: {channel.mention} as the audit-log-channel."


        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["config audit-log"].name}:",
                    mod_action,
                    False
                )
            ]
        )

        await channel.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(ConfigAuditLog(client))