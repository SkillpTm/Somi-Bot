import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import zoneinfo

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
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

        #TODO add to DB and get from db like weather lol

        if not timezone:
            timezone = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).timezone_get()

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/time",
            {"timezone": timezone}
        ))

        if not timezone in zoneinfo.available_timezones():
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please input a valid IANA timezone code."), ephemeral=True)
            return
        
        await interaction.response.defer(with_message=True)

        if timezone != await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).timezone_get():
            await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).timezone_set(timezone)
        
        currentTime = datetime.datetime.now(zoneinfo.ZoneInfo(timezone))
        utcOffset = currentTime.strftime("%z")

        # we want to format the offset to look like: +9, -4:30, +0
        if utcOffset[3] != "0":
            utcOffset = utcOffset[:-2] + ":" + utcOffset[-2:]
        else:
            utcOffset = utcOffset[:-2]

        if utcOffset[1] == "0":
            utcOffset = utcOffset[:1] + utcOffset[2:]

        if currentTime.hour >= 13:
            clockEmoji = f":clock{currentTime.hour-12}:"
        elif currentTime.hour == 0:
            clockEmoji = f":clock12:"
        else:
            clockEmoji = f":clock{currentTime.hour}:"

        embed = EmbedFunctions.builder(
            color = self.client.BOT_COLOR,
            author = currentTime.strftime(f"%Z (UTC {utcOffset})"),
            description = currentTime.strftime(f"# {clockEmoji} `%H:%M:%S`\n:calendar_spiral: `%Y/%m/%d`")
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