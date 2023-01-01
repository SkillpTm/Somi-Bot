####################################################################################################

import os
import time

####################################################################################################

from lib.utilities import SomiBot

client = SomiBot()

####################################################################################################

for folder in os.listdir(f"./cogs/"):
    if os.path.isdir(f"./cogs/{folder}/"):
        for file in os.listdir(f"./cogs/{folder}/"):
            if file.endswith(".py"):
                client.load_extension(f"cogs.{folder}.{file[:-3]}")

####################################################################################################

try:
    client.run(client.Keychain.DISCORD_TOKEN)
except:
    time.sleep(20)
    client.restart()