import datetime
import typing
import urllib.parse

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config, Keychain
from lib.modules import SomiBot



class Weather(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["weather"].name,
        Commands().data["weather"].description,
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
    async def weather(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        location: str = nextcord.SlashOption(
            Commands().data["weather"].parameters["location"].name,
            Commands().data["weather"].parameters["location"].description,
            required = False,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command outputs various statistics about the weather of any place (that's on openweathermap)"""

        db_location = str(await db.User.WEATHER.get(interaction.user.id))
        location = location or db_location
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={Keychain().WEATHER_API_KEY}&q={urllib.parse.quote_plus(location)}&units=metric", timeout=10)

        if response.status_code != 200:
            await interaction.send(embed=EmbedFunctions().get_error_message(f"{location} couldn't be found."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        if location != db_location:
            await db.User.WEATHER.set(interaction.user.id, location)

        response_json: dict[str, typing.Any] = response.json()
        output_data: dict[str, str] = {}

        # pull all the data we need from the json (and potentially format it, ready for the output)
        output_data["cloudiness"] = str(response_json["clouds"]["all"])
        output_data["country"] = Config().ISO_COUNTRY_TAGS[str(response_json["sys"]["country"])]
        output_data["descirption"] = str(response_json["weather"][0]["description"])
        output_data["humidity"] = str(response_json["main"]["humidity"])
        output_data["id"] = str(response_json["id"])
        output_data["local_time"] = datetime.datetime.fromtimestamp(response_json["dt"] + response_json["timezone"]).strftime("%H:%M:%S")
        output_data["metric_temp"] = str(round(response_json["main"]["temp"], 1))
        output_data["imperial_temp"] = str(round(response_json["main"]["temp"] * 9/5 + 32, 1)) # (0°C × 9/5) + 32 = 32°F
        output_data["metric_wind_speed"] = str(round(response_json["wind"]["speed"] * 3.6)) # m/s * 3.6 = km/h
        output_data["imperial_wind_speed"] = str(round(response_json["wind"]["speed"] * 3.6 * 1.609)) # km/h * 1,609 = mph
        output_data["name"] = str(response_json["name"])

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            title = f"Weather in: {output_data["name"]}, {output_data["country"]}",
            title_url = f"https://openweathermap.org/city/{output_data["id"]}",
            description = "\n".join([line.strip() for line in f"""
            ### {output_data["descirption"].title()}
            🕒 Local measurement time: `{output_data["local_time"]}`
            🌡️ Temperature: **{output_data["metric_temp"]} °C** ({output_data["imperial_temp"]} °F)
            💨 Wind: {output_data["metric_wind_speed"]} km/h ({output_data["imperial_wind_speed"]} mph)
            ☁️ Cloudiness: {output_data["cloudiness"]}%
            💧 Humidity: {output_data["humidity"]}%
            """.split("\n")]),
            footer = "Weather powered by OpenWeatherMap",
            footer_icon = Config().OPENWEATHERMAP_ICON
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Weather(client))