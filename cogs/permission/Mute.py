import datetime
import zoneinfo

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.events.MuteLog import MuteLog
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot



class Mute(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["mute"].name,
        Commands().data["mute"].description,
        default_member_permissions = nextcord.Permissions(mute_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def mute(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["mute"].parameters["member"].name,
            Commands().data["mute"].parameters["member"].description,
            required = True
        ),
        time: str = nextcord.SlashOption(
            Commands().data["mute"].parameters["time"].name,
            Commands().data["mute"].parameters["time"].description,
            required = True,
            min_length = 2,
            max_length = 50
        ),
        reason: str = nextcord.SlashOption(
            Commands().data["mute"].parameters["reason"].name,
            Commands().data["mute"].parameters["reason"].description,
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command mutes a member, with time and reason, if their current top-role is below your current top-role."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.send(embed=EmbedFunctions().get_error_message("You can't mute yourself!"))
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.guild.owner: # type: ignore
            await interaction.send(embed=EmbedFunctions().get_error_message("You can only mute a member, if your current top-role is above their current top-role!"))
            return

        total_seconds = Get.seconds_from_time(time)

        if not total_seconds or total_seconds > 2419200: #28d in seconds
            await interaction.send(embed=EmbedFunctions().get_error_message(f"`{time}` is not a valid time period. Make sure to use the formating in the input description and that your time period is smaller than 28 days."))
            return

        await member.edit(timeout=datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))+datetime.timedelta(seconds=total_seconds), reason=reason)
        await interaction.send(embed=EmbedFunctions().get_success_message(f"Succesfully muted {member.mention}."))
        await MuteLog.send_mute_log(interaction.user, member, reason) # type: ignore


    @nextcord.slash_command(
        Commands().data["unmute"].name,
        Commands().data["unmute"].description,
        default_member_permissions = nextcord.Permissions(mute_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def unmute(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["unmute"].parameters["member"].name,
            Commands().data["unmute"].parameters["member"].description,
            required = True
        ),
        reason: str = nextcord.SlashOption(
            Commands().data["unmute"].parameters["reason"].name,
            Commands().data["unmute"].parameters["reason"].description,
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command unmutes a member, if they were muted."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not member.communication_disabled_until:
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{member.mention} wasn't muted."))
            return

        await member.edit(timeout=None, reason=reason)
        await interaction.send(embed=EmbedFunctions().get_success_message(f"{member.mention} has been unmuted"))
        await MuteLog.send_unmute_log(interaction.user, member, reason) # type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(Mute(client))