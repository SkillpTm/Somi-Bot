import json
import os

import googleapiclient.discovery # type: ignore
import spotipy # type: ignore
import wolframalpha # type: ignore

from lib.managers.Singleton import Singleton



class Keychain(metaclass=Singleton):
    """Holds all the .env data on it"""

    def __init__(self):
        self.DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN") or ""

        self.DB_HOST: str = os.getenv("DB_HOST") or ""
        self.DB_PORT: int = int(os.getenv("DB_PORT") or 0)
        self.DB_USER: str = os.getenv("DB_USER") or ""
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD") or ""
        self.DB_NAME: str = os.getenv("DB_NAME") or ""

        self.SPOTIPY_CLIENT_ID: str = os.getenv("SPOTIPY_CLIENT_ID") or ""
        self.SPOTIPY_CLIENT_SECRET: str = os.getenv("SPOTIPY_CLIENT_SECRET") or ""
        self.SPOTIPY_REDIRECT_URI: str = os.getenv("SPOTIPY_REDIRECT_URI") or ""

        self.GENIUS_ACCESS_TOKEN: str = os.getenv("GENIUS_ACCESS_TOKEN") or ""
        self.LAST_FM_API_KEY: str = os.getenv("LAST_FM_API_KEY") or ""
        self.WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY") or ""
        self.WOLFRAM_APP_ID: str = os.getenv("WOLFRAM_APP_ID") or ""
        self.YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY") or ""

        # Webscraping cookies/headers to get around last.fm login
        self.LAST_FM_COOKIES: str = json.loads(os.getenv("LAST_FM_COOKIES") or "")
        self.LAST_FM_HEADERS: str = json.loads(os.getenv("LAST_FM_HEADERS") or "")

        self.spotify_oauth = spotipy.SpotifyOAuth(
            client_id = self.SPOTIPY_CLIENT_ID,
            client_secret = self.SPOTIPY_CLIENT_SECRET,
            redirect_uri = self.SPOTIPY_REDIRECT_URI,
            scope = "user-read-currently-playing"
        )

        self.wolfram_client = wolframalpha.Client(self.WOLFRAM_APP_ID)

        self.youtube = googleapiclient.discovery.build(
            "youtube",
            "v3",
            developerKey = self.YOUTUBE_API_KEY
        )