####################################################################################################

import datetime
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import pycountry
import requests

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Weather(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "weather", description = "find out what the weather is in any place")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def weather(self,
                      interaction: nextcord.Interaction,
                      *,
                      location: str = nextcord.SlashOption(description="the location you want to know the weather of", required=True, min_length=2, max_length=50)): #TODO store the locations and then use them for autocomplete
        """This command outputs various statistics about the weather of any place (that's on openweathermap)"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /weather {location}")

        location = location.replace(" ", "+")
        location = location.replace("#", "")

        request_url = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={self.client.Keychain.WEATHER_API_KEY}&q={location}&units=metric")

        if not request_url.status_code == 200:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{location} couldn't be found."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        weather_data: dict = request_url.json()

        weather_descirption: str = weather_data["weather"][0]["description"]
        humidity: int = weather_data["main"]["humidity"]
        cloud_percentage: int = weather_data["clouds"]["all"]
        location_time_utc: int = weather_data["dt"]
        country_code: str = weather_data["sys"]["country"]
        timezone_difference: int = weather_data["timezone"]
        location_name: str = weather_data["name"]

        current_temperature_metric: float = round(weather_data["main"]["temp"], 1)
        wind_speed_metric: float = round(weather_data["wind"]["speed"] * 3.6) #m/s * 3.6 = km/h

        current_temperature_imperial: float = round(current_temperature_metric * 9/5 + 32, 1) #(0°C × 9/5) + 32 = 32°F
        wind_speed_imperial: float = round(wind_speed_metric * 1.609) #km/h * 1,609 = mph

        country = pycountry.countries.get(alpha_2=country_code)

        local_date_and_time: str = datetime.datetime.utcfromtimestamp(location_time_utc + timezone_difference).strftime("%Y/%m/%d %H:%M:%S")
        local_date_and_time = local_date_and_time.split(" ")

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            title = f"Weather in: {location_name}, {country.name}",
            title_url = f"https://openweathermap.org/city/{weather_data['id']}",
            description = "\n".join([line.strip() for line in f"""
            **{weather_descirption}**
            🕒 Local measurement time: `{local_date_and_time[1]}`
            🌡️ Temperature: **{current_temperature_metric} °C** ({current_temperature_imperial} °F)
            💨 Wind: {wind_speed_metric} km/h ({wind_speed_imperial} mph)
            ☁️ Cloudiness: {cloud_percentage}%
            💧 Humidity: {humidity}%
            """.split("\n")]),
            footer = "Weather powered by OpenWeatherMap",
            footer_icon = self.client.OPENWEATHERMAP_ICON
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Weather(client))