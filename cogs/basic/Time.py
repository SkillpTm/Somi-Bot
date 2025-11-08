import datetime
import zoneinfo

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions, Get
from lib.managers import Config
from lib.utilities import SomiBot



class Time(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="time", description="shows the current time in any timezone")
    async def time(
        self,
        interaction: nextcord.Interaction,
        *,
        timezone: str = nextcord.SlashOption(
            description = "the IANA code timezone, you want the time of",
            required = False,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command will display the current date and time in any timezone"""

        timezone = timezone or await (await DBHandler(self.client.database, user_id=interaction.user.id).user()).timezone_get()

        if not timezone in zoneinfo.available_timezones():
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please input a valid IANA timezone code."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        if timezone != await (await DBHandler(self.client.database, user_id=interaction.user.id).user()).timezone_get():
            await (await DBHandler(self.client.database, user_id=interaction.user.id).user()).timezone_set(timezone)

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

        await interaction.followup.send(embed=embed)

    ####################################################################################################

    @time.on_autocomplete("timezone")
    async def time_autocomplete_timezone(
        self,
        interaction: nextcord.Interaction,
        timezone: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete_dict_from_search_string(
                timezone,
                {zone: zone for zone in sorted(zoneinfo.available_timezones())}
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(Time(client))