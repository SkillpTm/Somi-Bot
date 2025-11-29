import datetime
import zoneinfo

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Time(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["time"].name,
        Commands().data["time"].description,
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def time(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        timezone: str = nextcord.SlashOption(
            Commands().data["time"].parameters["timezone"].name,
            Commands().data["time"].parameters["timezone"].description,
            required = False,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command will display the current date and time in any timezone"""

        db_timezone = str(await db.User.TIMEZONE.get(interaction.user.id))
        timezone = timezone or db_timezone

        if timezone and timezone not in zoneinfo.available_timezones():
            await interaction.send(embed=EmbedFunctions.get_error_message("Please input a valid IANA timezone code."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        if timezone != db_timezone:
            await db.User.TIMEZONE.set(interaction.user.id, timezone)

        current_time = datetime.datetime.now(zoneinfo.ZoneInfo(timezone))
        offset_hours = current_time.utcoffset().total_seconds() / 3600

        # Format offset like: +9, -4:30, +0
        if offset_hours % 1 == 0:
            utc_offset = f"{offset_hours:+.0f}"
        else:
            utc_offset = f"{int(offset_hours):+d}:{int(abs(offset_hours % 1) * 60):02d}"

        clock_emoji = f":clock{current_time.hour % 12 or 12}:"

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            author = current_time.strftime(f"%Z (UTC {utc_offset})"),
            description = current_time.strftime(f"# {clock_emoji} `%H:%M:%S`\n:calendar_spiral: `%Y/%m/%d`")
        )

        await interaction.send(embed=embed)


    @time.on_autocomplete("timezone")
    async def time_autocomplete_timezone(
        self,
        interaction: nextcord.Interaction[SomiBot],
        timezone: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                timezone,
                sorted(zoneinfo.available_timezones())
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Time(client))