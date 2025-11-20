import os
import time

import requests

from lib.managers.Keychain import Keychain
from lib.modules.SomiBot import SomiBot



def load_cogs(client: SomiBot) -> None:
    """loads all cogs onto the client"""

    # crawl through ./cogs/ 's subfolders to load all cogs
    for folder in os.listdir("./cogs/"):
        if not os.path.isdir(f"./cogs/{folder}/"):
            continue

        for file in os.listdir(f"./cogs/{folder}/"):
            if not file.endswith(".py"):
                continue

            client.load_extension(f"cogs.{folder}.{file[:-3]}")


def start(client: SomiBot) -> None:
    """starts the bot indefinitly"""

    # if there is no internet connection indefinitly restart the bot
    try:
        if requests.get("https://www.google.com/", timeout=10).status_code == 200:
            client.run(Keychain().DISCORD_TOKEN)

    except KeyboardInterrupt:
        return

    except Exception as e:
        if (
            "ConnectionError" in str(type(e)) or # requests.ConnectionError
            "ClientConnectorError" in str(type(e)) # aiohttp.client_exceptions.ClientConnectorError
           ):
            time.sleep(10)
            client.restart()


if __name__ == "__main__":
    somi = SomiBot()

    load_cogs(somi)
    start(somi) # blocks until the bot is shutdown