from dataclasses import dataclass
import json
import os



@dataclass
class Keychain():
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")

    SPOTIPY_CLIENT_ID: str = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET: str = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI: str = os.getenv("SPOTIPY_REDIRECT_URI")

    GENIUS_ACCESS_TOKEN: str = os.getenv("GENIUS_ACCESS_TOKEN")
    LAST_FM_API_KEY: str = os.getenv("LAST_FM_API_KEY")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")
    WOLFRAM_APP_ID: str = os.getenv("WOLFRAM_APP_ID")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY")

    # Webscraping
    LAST_FM_COOKIES = json.loads(os.getenv("LAST_FM_COOKIES"))
    LAST_FM_HEADERS = json.loads(os.getenv("LAST_FM_HEADERS"))