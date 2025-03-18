import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import pycountry
import requests

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Weather(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="weather", description="find out what the weather is in any place")
    async def weather(
        self,
        interaction: nextcord.Interaction,
        *,
        location: str = nextcord.SlashOption(
            description = "the location you want to know the weather of",
            required = False,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command outputs various statistics about the weather of any place (that's on openweathermap)"""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/weather",
            {"location": location}
        ))

        input_location = location # in case we error on the api call later we need the original input for the error message
        location = location.lower().replace(" ", "+").replace("#", "")

        if location:
            await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).weather_set(location)

        # if no location was provided we either get the last submitted one or the default value 'seoul'
        location = await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).weather_get()

        await interaction.response.defer(with_message = True)

        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={self.client.Keychain.WEATHER_API_KEY}&q={location}&units=metric")

        if response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"{input_location} couldn't be found."), ephemeral=True)
            return

        response_json: dict = response.json()
        output_data: dict[str, str] = {}

        # pull all the data we need from the json (and potentially format it, ready for the output)
        output_data["cloudiness"] = str(response_json["clouds"]["all"])
        output_data["country"] = pycountry.countries.get(alpha_2=str(response_json["sys"]["country"])).name
        output_data["descirption"] = str(response_json["weather"][0]["description"])
        output_data["humidity"] = str(response_json["main"]["humidity"])
        output_data["id"] = str(response_json['id'])
        output_data["local_time"] = datetime.datetime.fromtimestamp(response_json["dt"] + response_json["timezone"]).strftime("%H:%M:%S")
        output_data["metric_temp"] = str(round(response_json["main"]["temp"], 1))
        output_data["imperial_temp"] = str(round(response_json["main"]["temp"] * 9/5 + 32, 1)) #(0°C × 9/5) + 32 = 32°F
        output_data["metric_wind_speed"] = str(round(response_json["wind"]["speed"] * 3.6)) #m/s * 3.6 = km/h
        output_data["imperial_wind_speed"] = str(round(response_json["wind"]["speed"] * 3.6 * 1.609)) #km/h * 1,609 = mph
        output_data["name"] = str(response_json["name"])

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            title = f"Weather in: {output_data["name"]}, {output_data["country"]}",
            title_url = f"https://openweathermap.org/city/{output_data["id"]}",
            description = "\n".join([line.strip() for line in f"""
            **{output_data["descirption"]}**
            🕒 Local measurement time: `{output_data["local_time"]}`
            🌡️ Temperature: **{output_data["metric_temp"]} °C** ({output_data["imperial_temp"]} °F)
            💨 Wind: {output_data["metric_wind_speed"]} km/h ({output_data["imperial_wind_speed"]} mph)
            ☁️ Cloudiness: {output_data["cloudiness"]}%
            💧 Humidity: {output_data["humidity"]}%
            """.split("\n")]),
            footer = "Weather powered by OpenWeatherMap",
            footer_icon = self.client.OPENWEATHERMAP_ICON
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Weather(client))