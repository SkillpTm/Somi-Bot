from dataclasses import dataclass
import dotenv
import json
import os



@dataclass
class Keychain():
    dotenv.load_dotenv()

    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    
    LAST_FM_API_KEY: str = os.getenv("LAST_FM_API_KEY")

    with open('env.json') as env_json:
        env_json_data = json.loads(env_json.read())
    
    LAST_FM_COOKIES = env_json_data["LAST_FM_COOKIES"]
    LAST_FM_HEADERS = env_json_data["LAST_FM_HEADERS"]

    SPOTIPY_CLIENT_ID: str = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET: str = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI: str = os.getenv("SPOTIPY_REDIRECT_URI")

    GENIUS_ACCESS_TOKEN: str = os.getenv("GENIUS_ACCESS_TOKEN")

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    WOLFRAM_APP_ID: str = os.getenv("WOLFRAM_APP_ID")

    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY")