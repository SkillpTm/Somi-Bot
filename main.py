import aiohttp.client_exceptions
import os
import requests
import time

from lib.utilities import SomiBot

client = SomiBot()

####################################################################################################

def load_Cogs() -> None:
    """loads all cogs onto the client"""

    # crawl through ./cogs/ 's subfolders to load all cogs
    for folder in os.listdir(f"./cogs/"):
        if not os.path.isdir(f"./cogs/{folder}/"):
            continue
        
        for file in os.listdir(f"./cogs/{folder}/"):
            if not file.endswith(".py"):
                continue

            client.load_extension(f"cogs.{folder}.{file[:-3]}")

####################################################################################################

def start() -> None:
    """starts the bot indefinitly"""

    # if there is no internet connection indefinitly restart the bot
    try:
        if requests.get("https://www.google.com/").status_code == 200:
            client.run(client.Keychain.DISCORD_TOKEN)
    except (requests.ConnectionError, aiohttp.client_exceptions.ClientConnectorError):
        time.sleep(10)
        client.restart()

####################################################################################################

if __name__ == "__main__":
    load_Cogs()
    start() # blocks until the bot is shutdown