<h2>Information</h2>

<h4>Base information</h4>

Somi#6418 is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
Originally it was created to fullfil all needs of Somicord.

<h4>Created by:</h4>
skillp

<h4>Current version:</h4>
3.0

<h4>Invites:</h4>
There are currently no plans to have public invites. You might get an invite by asking skillp.

<h4>Issues:</h4>
You can report bugs and make suggestions with /feedback

<h2>Cloning</h2>

This repo isn't inherintly meant for you to clone it and spin up your own version. If you still want to do that, follow these steps:

1. Replace the information in .\storage\config.py with the one of your bot.
2. Make a .env at .\\.env with these variables:

```sh
# https://discord.com/developers/applications
DISCORD_TOKEN="ENTER VALUE"

# https://www.last.fm/api
LAST_FM_USERNAME = "ENTER VALUE"
LAST_FM_PASSWORD = "ENTER VALUE"
LAST_FM_API_KEY = "ENTER VALUE"
LAST_FM_API_SECRET = "ENTER VALUE"

# https://developer.spotify.com/
SPOTIPY_CLIENT_ID="ENTER VALUE"
SPOTIPY_CLIENT_SECRET="ENTER VALUE"
SPOTIPY_REDIRECT_URI="ENTER VALUE"

# https://docs.genius.com/
GENIUS_ACCESS_TOKEN="ENTER VALUE"

# https://openweathermap.org/api
WEATHER_API_KEY="ENTER VALUE"

# https://products.wolframalpha.com/api
WOLFRAM_APP_ID="ENTER VALUE"

# https://developers.google.com/docs/api/quickstart/python
YOUTUBE_API_KEY="ENTER VALUE"
```

3. Make a json file at .\env.json with these variables:

```sh
# On how to get this checkout this comment https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup/61140905#61140905
LAST_FM_COOKIES = {
    'ENETER VALUES': 'ENETER VALUES',
}
LAST_FM_HEADERS = {
    'ENETER VALUES': 'ENETER VALUES',
}
```

4. Now run the bot:

```sh
py .\main.py
```