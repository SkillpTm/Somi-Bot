###package#import###############################################################################

import datetime
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import os
import pycountry
import requests
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import BOT_COLOR, OPENWEATHERMAP_ICON



class weather(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###weather###########################################################

    @nextcord.slash_command(name = "weather", description = "find out what the weather is in any place")
    async def weather(self,
                      interaction: Interaction,
                      *,
                      location: str = SlashOption(description="the location you want to know thw weather of", required=True, min_length=1, max_length=30)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /weather {location}")

        location = location.replace(" ", "+")
        location = location.replace("#", "")

        API_KEY = os.getenv("WEATHER_API_KEY")

        request_url = f"http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={location}&units=metric"

        if not requests.get(request_url).status_code == 200:
            await interaction.response.send_message("Your selected location couldn't be found.", ephemeral=True)
            return

        weather_data = requests.get(request_url).json()

        descirption = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        cloud_percentage = weather_data["clouds"]["all"]
        location_time_utc = weather_data["dt"]
        country_code = weather_data["sys"]["country"]
        timezone_difference = weather_data["timezone"]
        location_name = weather_data["name"]

        current_temperature_metric = round(weather_data["main"]["temp"], 1)
        wind_speed_metric = round(weather_data["wind"]["speed"] * 3.6) #m/s * 3.6 = km/h

        current_temperature_imperial = round(current_temperature_metric * 9/5 + 32, 1) #(0°C × 9/5) + 32 = 32°F
        wind_speed_imperial = round(wind_speed_metric * 1.609) #km/h * 1,609 = mph

        country = pycountry.countries.get(alpha_2=country_code)

        format = "%Y/%m/%d %H:%M:%S"
        unformated_time = datetime.datetime.fromtimestamp(location_time_utc + timezone_difference - 7200) #For some reason all times are 2h off, this fixes it
        local_date_and_time = unformated_time.strftime(format)
        local_date_and_time = local_date_and_time.split(" ")

        output = f"""
        **{descirption}**
        🕒 Local measurement time: `{local_date_and_time[1]}`
        🌡️ Temperature: **{current_temperature_metric} °C** ({current_temperature_imperial} °F)
        💨 Wind: {wind_speed_metric} km/h ({wind_speed_imperial} mph)
        ☁️ Cloudiness: {cloud_percentage}%
        💧 Humidity: {humidity}%
        """

        embed = embed_builder(title = f"Weather for: {location_name}, {country.name}",
                              title_url = f"https://openweathermap.org/city/{weather_data['id']}",
                              description = output,
                              color = BOT_COLOR,
                              footer = "Weather powered by OpenWeatherMap",
                              footer_icon = OPENWEATHERMAP_ICON)

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "weather")

def setup(client):
    client.add_cog(weather(client))