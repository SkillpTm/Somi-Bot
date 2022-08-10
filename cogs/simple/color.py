###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from PIL import Image
from PIL import ImageColor
import os

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder



class color(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###color###########################################################

    @nextcord.slash_command(name = "color", description = "shows you what a color looks like")
    async def color(self,
                    interaction: Interaction,
                    *,
                    hexcode: str = SlashOption(description="input a color hexcode here (either with or without the #)", required=True, min_length=6, max_length=7)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /color {hexcode}")

        if not hexcode.startswith("#"):
            hexcode = f"#{hexcode}"

        try:
            hex_rgb = ImageColor.getcolor(hexcode, "RGB")
        except:
            await interaction.response.send_message("Please input a valid hex value for a color.", ephemeral=True)
            return

        for i in range(len(hex_rgb)):
            if hex_rgb[i] < 0 or hex_rgb[i] > 256:
                await interaction.response.send_message("Please input a valid hex value for a color.", ephemeral=True)
                return

        color_image = Image.new('RGB', (400, 400), hex_rgb)

        color_image.save(f"./storage/temp/{hexcode}.png")

        embed = embed_builder(title = f"Color: {hexcode}",
                              color = int(f"0x{hexcode}"),
                              image = f"./storage/temp/{hexcode}.png")

        await interaction.response.send_message(embed=embed)

        os.remove("demofile.txt")

        uses_update(f"./storage/temp/{hexcode}.png")

def setup(client):
    client.add_cog(color(client))