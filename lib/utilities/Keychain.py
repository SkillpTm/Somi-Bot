####################################################################################################

from dataclasses import dataclass
import dotenv
import os

####################################################################################################


@dataclass
class Keychain():
    dotenv.load_dotenv()

    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    
    LAST_FM_USERNAME: str = os.getenv("LAST_FM_USERNAME")
    LAST_FM_PASSWORD: str = os.getenv("LAST_FM_PASSWORD")
    LAST_FM_API_KEY: str = os.getenv("LAST_FM_API_KEY")
    LAST_FM_API_SECRET: str = os.getenv("LAST_FM_API_SECRET")
    
    LAST_FM_COOKIES: str = os.getenv("LAST_FM_COOKIES")

    REDDIT_ID: str = os.getenv("REDDIT_ID")
    REDDIT_SECRET: str = os.getenv("REDDIT_SECRET")
    REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD")

    SPOTIPY_CLIENT_ID: str = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET: str = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI: str = os.getenv("SPOTIPY_REDIRECT_URI")

    GENIUS_ACCESS_TOKEN: str = os.getenv("GENIUS_ACCESS_TOKEN")

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    WOLFRAM_APP_ID: str = os.getenv("WOLFRAM_APP_ID")