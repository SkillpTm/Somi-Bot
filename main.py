####################################################################################################

import os

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

client.run(client.Keychain.DISCORD_TOKEN)