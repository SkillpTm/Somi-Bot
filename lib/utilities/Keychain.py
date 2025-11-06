import dataclasses
import json
import os



@dataclasses.dataclass
class Keychain():
    """Holds all the .env data on it"""

    DISCORD_TOKEN: str = dataclasses.field(default_factory = lambda: os.getenv("DISCORD_TOKEN"))

    SPOTIPY_CLIENT_ID: str = dataclasses.field(default_factory = lambda: os.getenv("SPOTIPY_CLIENT_ID"))
    SPOTIPY_CLIENT_SECRET: str = dataclasses.field(default_factory = lambda: os.getenv("SPOTIPY_CLIENT_SECRET"))
    SPOTIPY_REDIRECT_URI: str = dataclasses.field(default_factory = lambda: os.getenv("SPOTIPY_REDIRECT_URI"))

    GENIUS_ACCESS_TOKEN: str = dataclasses.field(default_factory = lambda: os.getenv("GENIUS_ACCESS_TOKEN"))
    LAST_FM_API_KEY: str = dataclasses.field(default_factory = lambda: os.getenv("LAST_FM_API_KEY"))
    WEATHER_API_KEY: str = dataclasses.field(default_factory = lambda: os.getenv("WEATHER_API_KEY"))
    WOLFRAM_APP_ID: str = dataclasses.field(default_factory = lambda: os.getenv("WOLFRAM_APP_ID"))
    YOUTUBE_API_KEY: str = dataclasses.field(default_factory = lambda: os.getenv("YOUTUBE_API_KEY"))

    # Webscraping cookies/headers to get around last.fm login
    LAST_FM_COOKIES: str = dataclasses.field(default_factory = lambda: json.loads(os.getenv("LAST_FM_COOKIES")))
    LAST_FM_HEADERS: str = dataclasses.field(default_factory = lambda: json.loads(os.getenv("LAST_FM_HEADERS")))