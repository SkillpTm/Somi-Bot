####################################################################################################

import aiohttp.client_exceptions
import os
import requests
import time

####################################################################################################

from lib.utilities import SomiBot

client = SomiBot()

####################################################################################################

for folder in os.listdir(f"./cogs/"):
    if not os.path.isdir(f"./cogs/{folder}/"):
        continue
    
    for file in os.listdir(f"./cogs/{folder}/"):
        if not file.endswith(".py"):
            continue

        client.load_extension(f"cogs.{folder}.{file[:-3]}")

####################################################################################################

try:
    requests.get("https://www.google.com/")
    client.run(client.Keychain.DISCORD_TOKEN)
except (requests.ConnectionError, aiohttp.client_exceptions.ClientConnectorError):
    time.sleep(10)
    client.restart()